"""Perception-Decision-Action main loop for Panda Pick & Place.

Runs a closed-loop control flow where an Agent decides the next macro-action
based on the current environment state. Two modes are supported:

* ``demo`` – a hard-coded state-machine policy (no API key needed).
* ``llm``  – LLM agent via function calling (OpenAI/OpenRouter SDK compatible).

Usage
-----
    python main.py --mode demo                    # Run built-in demo policy
    python main.py --mode llm --provider openai   # Use OpenAI API
    python main.py --mode llm --provider openrouter  # Use OpenRouter API

Environment variables
---------------------
OPENAI_API_KEY       Required for OpenAI provider.
OPENROUTER_API_KEY   Required for OpenRouter provider.
LLM_MODEL            Model name (default: ``gpt-4o-mini`` for OpenAI, 
                     ``meta-llama/llama-2-70b-chat`` for OpenRouter).
"""

import argparse
import json
import os
import time
from typing import Callable, Dict, List, Union

from skills import (
    close_skills,
    get_state_dict,
    grasp,
    move_arm_to,
    perceive_environment,
    release,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
GRIP_HEIGHT_OFFSET = 0.03   # metres above object centre
HOVER_HEIGHT_OFFSET = 0.10

# ---------------------------------------------------------------------------
# Demo state machine globals (mutated by demo_policy)
# ---------------------------------------------------------------------------
_demo_phase: str = "OPEN_GRIPPER"
_holding_object: bool = False


def _current_state() -> Dict[str, Union[List[float], float, bool]]:
    """Shorthand for the numeric state dict."""
    return get_state_dict()  # type: ignore[return-value]


def _dist(a: List[float], b: List[float]) -> float:
    """Euclidean distance between two 3-D points."""
    return float(sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5)


def _check_holding(s: Dict[str, Union[List[float], float, bool]]) -> bool:
    """Heuristic: have we successfully grasped the cube?

    In this simulation the gripper closes to ~3 cm, which is slightly
    narrower than the 4 cm cube. The cube therefore wedges the fingers
    open to ≈4 cm. We detect a successful grasp when the cube has been
    lifted off the table (>3 cm) and the fingers are wedged open.

    Must be called *after* the arm has lifted the cube.
    """
    obj: List[float] = s["object_position"]  # type: ignore[assignment]
    fingers: float = s["gripper_width"]  # type: ignore[assignment]
    return (
        0.02 <= fingers <= 0.06
        and obj[2] > 0.03
    )


def demo_policy(_: int) -> str:
    """Hard-coded pick-and-place state-machine.

    Runs one FSM transition per call, mutating the global ``_demo_phase``.

    Returns:
        A human-readable description of the chosen action.
    """
    global _demo_phase, _holding_object

    s = _current_state()
    ee: List[float] = s["ee_position"]  # type: ignore[assignment]
    obj: List[float] = s["object_position"]  # type: ignore[assignment]
    goal: List[float] = s["target_position"]  # type: ignore[assignment]
    fingers: float = s["gripper_width"]  # type: ignore[assignment]

    # ---- Phase 1: open gripper ------------------------------------------------
    if _demo_phase == "OPEN_GRIPPER":
        if fingers >= 0.06:
            _demo_phase = "ABOVE_OBJ"
            return "Demo: Gripper already open, heading to object."
        release()
        if fingers >= 0.06:
            _demo_phase = "ABOVE_OBJ"
        return "Demo: Opening gripper."

    # ---- Phase 2: move above object ------------------------------------------
    if _demo_phase == "ABOVE_OBJ":
        above = [obj[0], obj[1], obj[2] + HOVER_HEIGHT_OFFSET]
        if _dist(ee, above) < 0.02 and ee[2] > above[2] - 0.03:
            _demo_phase = "DESCEND_OBJ"
            return "Demo: Reached hover, descending to grip height."
        move_arm_to(*above)
        return f"Demo: Moving above object {above}."

    # ---- Phase 3: descend to object -----------------------------------------
    if _demo_phase == "DESCEND_OBJ":
        grip = [obj[0], obj[1], obj[2] + GRIP_HEIGHT_OFFSET]
        if _dist(ee, grip) < 0.015 and ee[2] < grip[2] + 0.01:
            _demo_phase = "GRASP"
            return "Demo: At grip height, initiating grasp."
        move_arm_to(*grip)
        return f"Demo: Descending to {grip}."

    # ---- Phase 4: close gripper (single attempt) ----------------------------
    if _demo_phase == "GRASP":
        grasp()
        _demo_phase = "LIFT"
        return "Demo: Gripper closed, initiating lift."

    # ---- Phase 5: lift and verify -------------------------------------------
    if _demo_phase == "LIFT":
        lift_target = [obj[0], obj[1], obj[2] + HOVER_HEIGHT_OFFSET + 0.05]
        if _dist(ee, lift_target) < 0.02:
            s_after = _current_state()
            _holding_object = _check_holding(s_after)
            if _holding_object:
                _demo_phase = "TRANSPORT"
                return "Demo: Lift verified, cube is held. Transporting to target."
            # Cube slipped – back off and retry
            _demo_phase = "ABOVE_OBJ"
            release()
            return "Demo: Cube slipped during lift, retrying."
        move_arm_to(*lift_target)
        return f"Demo: Lifting to {lift_target}."

    # ---- Phase 6: transport above goal --------------------------------------
    if _demo_phase == "TRANSPORT":
        s_after = _current_state()
        if not _check_holding(s_after):
            _holding_object = False
            _demo_phase = "ABOVE_OBJ"
            release()
            return "Demo: Cube lost during transport, retrying."
        above_goal = [goal[0], goal[1], goal[2] + HOVER_HEIGHT_OFFSET]
        if _dist([ee[0], ee[1]], [goal[0], goal[1]]) < 0.02 and ee[2] > above_goal[2] - 0.03:
            _demo_phase = "DESCEND_GOAL"
            return "Demo: Over target, lowering."
        move_arm_to(*above_goal)
        return f"Demo: Transporting above target {above_goal}."

    # ---- Phase 7: lower onto goal -------------------------------------------
    if _demo_phase == "DESCEND_GOAL":
        drop = [goal[0], goal[1], goal[2] + GRIP_HEIGHT_OFFSET]
        if _dist(ee, drop) < 0.02 and ee[2] < drop[2] + 0.02:
            _demo_phase = "RELEASE"
            return "Demo: Ready to release."
        move_arm_to(*drop)
        return f"Demo: Lowering to drop point {drop}."

    # ---- Phase 8: release ---------------------------------------------------
    if _demo_phase == "RELEASE":
        release()
        _holding_object = False
        _demo_phase = "DONE"
        return "Demo: Object released at target. Done."

    return "Demo: Idle."


# ===========================================================================
# 2. LLM-POWERED AGENT  (OpenAI function calling)
# ===========================================================================


def _build_tools() -> List[Dict[str, Union[str, Dict]]]:
    """Return the tool schemas for OpenAI Chat Completions API."""
    return [
        {
            "type": "function",
            "function": {
                "name": "perceive_environment",
                "description": (
                    "Get a textual snapshot of the scene: robot end-effector "
                    "position, gripper width, object position, target position, and task success flag."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "move_arm_to",
                "description": (
                    "Move the robot end-effector to an absolute (x, y, z) position "
                    "in metres. Typical workspace: x∈[-1.0,0.2], y∈[-0.6,0.6], z∈[0.0,1.2]."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x": {"type": "number", "description": "Target X coordinate."},
                        "y": {"type": "number", "description": "Target Y coordinate."},
                        "z": {"type": "number", "description": "Target Z coordinate."},
                    },
                    "required": ["x", "y", "z"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "grasp",
                "description": "Close the gripper to try and pick up the object.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "release",
                "description": "Open the gripper to drop the object.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False,
                },
            },
        },
    ]


_TOOL_MAP: Dict[str, Callable] = {
    "perceive_environment": perceive_environment,
    "move_arm_to": move_arm_to,
    "grasp": grasp,
    "release": release,
}


def llm_policy(
    client,
    model: str,
    messages: List[Dict[str, str]],
    max_steps: int = 30,
) -> List[Dict[str, str]]:
    """Run the LLM agent loop with tool calling enabled.

    Args:
        client: An ``openai.OpenAI`` client instance.
        model: Model identifier, e.g. ``gpt-4o-mini``.
        messages: Mutable conversation history.
        max_steps: Maximum number of tool interactions before exiting.

    Returns:
        The updated *messages* list.
    """
    tools = _build_tools()

    print("\n--- Starting LLM loop (max {} steps) ---".format(max_steps))
    for step in range(max_steps):
        response = client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore[arg-type]
            tools=tools,  # type: ignore[arg-type]
            tool_choice="auto",
            temperature=0.0,
        )
        message = response.choices[0].message
        messages.append(message.model_dump())

        # ---- Content-only (no tool call) --------------------------------
        if not message.tool_calls:
            print(f"[LLM {step}] {message.content}")
            if "done" in (message.content or "").lower():
                break
            continue

        # ---- Execute tool calls -----------------------------------------
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            raw_args = tool_call.function.arguments or "{}"
            try:
                args: Dict[str, Union[float, int]] = json.loads(raw_args)
            except json.JSONDecodeError:
                args = {}
            print(f"[LLM {step}] Calling {func_name}({args})")
            tool_func = _TOOL_MAP[func_name]
            result = tool_func(**args)
            print(f"[LLM {step}] -> {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": func_name,
                "content": result,
            })

        # Early stop if user dropped the object near the target
        state = _current_state()
        if state.get("success", False):
            print("\n--- Task success detected! Exiting loop. ---")
            break

        time.sleep(0.5)

    return messages


# ===========================================================================
# 3. MAIN
# ===========================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description="Panda Pick & Place closed-loop demo")
    parser.add_argument(
        "--mode",
        choices=["demo", "llm"],
        default="demo",
        help="Control mode: demo=hard-coded policy, llm=LLM function calling",
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "openrouter"],
        default="openrouter",
        help="LLM service provider: openai or openrouter (default: openrouter)",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=40,
        help="Maximum number of decision steps (default: 40).",
    )
    args = parser.parse_args()

    if args.mode == "llm":
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "openai SDK not installed. Run:  pip install openai"
            ) from exc

        # ---- Configure based on provider ------------------------------------
        if args.provider == "openrouter":
            api_key = os.environ.get("OPENROUTER_API_KEY", "")
            if not api_key:
                raise RuntimeError(
                    "OPENROUTER_API_KEY is required for --provider openrouter. "
                    "Set it as an env var or pass it via --api-key."
                )
            base_url = "https://openrouter.ai/api/v1"
            # Using models verified to work in your region
            # Default: mistralai/mistral-large | Alternative: deepseek/deepseek-chat
            model = os.environ.get("LLM_MODEL", "deepseek/deepseek-v4-flash")
            print(f"Using OpenRouter API with model: {model}")

        else:  # openai
            api_key = os.environ.get("OPENAI_API_KEY", "")
            if not api_key:
                raise RuntimeError(
                    "OPENAI_API_KEY is required for --provider openai. "
                    "Set it as an env var."
                )
            base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
            model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
            print(f"Using OpenAI API with model: {model}")

        client = OpenAI(api_key=api_key, base_url=base_url)
        
        # For OpenRouter, we should add required headers
        if args.provider == "openrouter":
            # OpenRouter requires these headers
            client.default_headers["HTTP-Referer"] = "https://github.com/your-username/robot_agent"
            client.default_headers["X-Title"] = "Panda Robot Pick & Place"

        system_prompt = (
            "You are a robotic manipulation planner for a Franka Panda arm in a Pick & Place task.\n"
            "The scene contains a green cube (object) and an invisible target (goal).\n"
            "You have 4 tools: perceive_environment(), move_arm_to(x,y,z), grasp(), release().\n"
            "Coordinates are in metres. Workspace: x∈[-1.0, 0.2], y∈[-0.6, 0.6], z∈[0.0, 1.2].\n"
            "\n"
            "CRITICAL GRASPING RULES:\n"
            "The object_position returned by the environment is the geometric center of the cube. "
            "If you try to grasp at this exact Z-coordinate, the object will slip. "
            "To grasp securely, your final descent Z-coordinate MUST be exactly (object_z - 0.015).\n"
            "\n"
            "Strategy (Strict SOP):\n"
            "1. Perceive: Call perceive_environment() to get object and target coordinates.\n"
            "2. Prepare: Call release() to ensure the gripper is open.\n"
            "3. Hover: move_arm_to(object_x, object_y, object_z + 0.10) to safely position above the cube.\n"
            "4. Descend: move_arm_to(object_x, object_y, object_z - 0.015) to wedge fingers against the cube.\n"
            "5. Grasp: Call grasp().\n"
            "6. Lift & Move: move_arm_to(target_x, target_y, target_z + 0.10) to move safely above the goal.\n"
            "7. Place: move_arm_to(target_x, target_y, target_z) and call release().\n"
            "8. Finish: Reply exactly with 'done' and stop calling tools."
        )

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt},
        ]
        print("Initial perception:")
        print(perceive_environment())
        messages.append({"role": "user", "content": "Start picking and placing the cube."})
        llm_policy(client, model, messages, max_steps=args.max_steps)
        print("\n=== Final state ===")
        print(perceive_environment())

    else:  # demo mode
        global _demo_phase, _holding_object
        _demo_phase = "OPEN_GRIPPER"
        _holding_object = False

        print("Running DEMO policy (no API key needed).\n")
        print("Initial perception:")
        print(perceive_environment())

        for step in range(args.max_steps):
            print(f"\n--- Step {step} ---")
            action_desc = demo_policy(step)
            print(action_desc)

            if _demo_phase == "DONE":
                break

            # Also use the official success metric (object within 5 cm of goal)
            if _current_state().get("success", False):
                print("\n--- Task success! ---")
                break

            time.sleep(0.3)

        print("\n=== Final state ===")
        print(perceive_environment())

    close_skills()
    print("Simulation closed.")


if __name__ == "__main__":
    main()
