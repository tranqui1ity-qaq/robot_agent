"""Record LLM-driven robot demo as MP4 video file.

Usage:
    python record_video.py --max-steps 50 --fps 60 --frames-per-step 50 --provider openrouter
    python record_video.py --output demo.mp4 --provider openai --max-steps 30

关键概念：
- 每个 LLM 决策 step 会调用一个工具（move_arm_to/grasp/release 等）
- 我们在每个工具执行后都捕 frames_per_step 帧
- frames_per_step 越大 = 视频越长/越流畅
"""

import argparse
import json
import os
import sys
from typing import List, Dict, Union

def record_llm_video(
    output: str = "robot_llm.mp4",
    max_steps: int = 50,
    fps: int = 60,
    frames_per_step: int = 20,
    provider: str = "openrouter",
):
    """Record LLM mode as video.
    
    Args:
        output: Output video filename
        max_steps: Maximum LLM decision steps
        fps: Video frames per second
        frames_per_step: Frames captured per LLM tool call
        provider: LLM provider ('openrouter' or 'openai')
    """
    import numpy as np
    try:
        import cv2
    except ImportError:
        print("Error: opencv-python not installed. Run: pip install opencv-python")
        return
    
    from openai import OpenAI
    from skills import perceive_environment, close_skills, _ensure_initialized
    from main import _current_state, _build_tools, _TOOL_MAP
    
    print(f"Initializing LLM video recording...")
    print(f"  Provider: {provider}")
    print(f"  FPS: {fps}")
    print(f"  Frames per tool call: {frames_per_step}")
    print(f"  Max LLM steps: {max_steps}")
    print()
    
    os.makedirs("videos", exist_ok=True)
    output_path = f"videos/{output}"
    
    frames: List[np.ndarray] = []
    
    # Initialize client based on provider
    if provider == "openrouter":
        api_key = os.environ.get("OPENROUTER_API_KEY", "")
        if not api_key:
            print("Error: OPENROUTER_API_KEY not set")
            print("Please set it with: export OPENROUTER_API_KEY='your-key-here'")
            return
        
        client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        client.default_headers["HTTP-Referer"] = "https://github.com/tranqui1ity-qaq/robot_agent"
        client.default_headers["X-Title"] = "Panda Robot Pick & Place"
        model = os.environ.get("LLM_MODEL", "mistralai/mistral-large")
        
    elif provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            print("Error: OPENAI_API_KEY not set")
            print("Please set it with: export OPENAI_API_KEY='your-key-here'")
            return
        
        client = OpenAI(api_key=api_key)
        model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
    else:
        print(f"Error: Unknown provider '{provider}'. Use 'openrouter' or 'openai'")
        return
    
    print(f"Using model: {model}")
    print()
    
    # Initialize environment
    print("Starting perception...")
    perceive_environment()
    controller = _ensure_initialized()
    
    tools = _build_tools()
    system_prompt = (
        "You are a robotic manipulation planner for a Franka Panda arm in a Pick & Place task.\n"
        "Goal: Pick up a green cube and place it at the target location.\n"
        "Tools available: perceive_environment, move_arm_to(x,y,z), grasp, release.\n\n"
        "STRICT RULES:\n"
        "- Make EXACTLY ONE tool call per response. Never combine multiple calls.\n"
        "- Always put the tool call in proper function format.\n"
        "- Maintain a careful sequence:\n"
        "  1. perceive_environment - get positions\n"
        "  2. release - open gripper\n"
        "  3. move_arm_to above cube (z = cube_z + 0.12)\n"
        "  4. move_arm_to to cube (z = cube_z + 0.03)\n"
        "  5. grasp - close gripper\n"
        "  6. move_arm_to lift position (z = cube_z + 0.15)\n"
        "  7. move_arm_to above target (z = target_z + 0.12)\n"
        "  8. move_arm_to to target (z = target_z + 0.03)\n"
        "  9. release - drop cube\n"
        "  10. perceive_environment - verify success\n"
        "- Do NOT skip steps.\n"
        "- When task is complete (cube at target), reply 'Task completed successfully!'\n"
        "- Workspace: x∈[-1.0,0.2], y∈[-0.6,0.6], z∈[0.0,1.2]"
    )
    
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt},
    ]
    
    print("Initial perception:")
    print(perceive_environment())
    messages.append({"role": "user", "content": "Start picking and placing the cube."})
    
    print(f"\nRecording LLM loop (max {max_steps} steps)...\n")
    tool_call_count = 0
    
    for step in range(max_steps):
        # LLM decision
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.0,
        )
        message = response.choices[0].message
        messages.append(message.model_dump())
        
        if not message.tool_calls:
            print(f"[Step {step}] LLM: {message.content}")
            if "done" in (message.content or "").lower():
                break
            continue
        
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            raw_args = tool_call.function.arguments or "{}"
            try:
                args: Dict[str, Union[float, int]] = json.loads(raw_args)
            except json.JSONDecodeError:
                args = {}
            
            print(f"[Step {step}] → {func_name}({args})")
            tool_call_count += 1
            
            # Execute tool
            tool_func = _TOOL_MAP[func_name]
            result = tool_func(**args)
            
            # Capture frames after tool execution
            for _ in range(frames_per_step):
                rgb = controller.env.render()
                if rgb is not None and len(rgb) > 0:
                    frames.append(rgb.copy())
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": func_name,
                "content": result,
            })
        
        if _current_state().get("success", False):
            print("\n✓ Task success detected!")
            break
    
    # Capture final frames
    print("Capturing final frames...")
    for _ in range(frames_per_step * 2):
        rgb = controller.env.render()
        if rgb is not None and len(rgb) > 0:
            frames.append(rgb.copy())
    
    close_skills()
    
    if frames:
        print(f"\nEncoding video...")
        print(f"  Tool calls: {tool_call_count}")
        print(f"  Total frames: {len(frames)}")
        print(f"  FPS: {fps}")
        print(f"  Duration: {len(frames) / fps:.2f} seconds")
        print(f"  Output: {output_path}")
        
        height, width = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        for i, frame in enumerate(frames):
            frame_bgr = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_RGB2BGR)
            out.write(frame_bgr)
            if (i + 1) % 150 == 0:
                print(f"  Encoded {i + 1}/{len(frames)} frames")
        
        out.release()
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"\n✓ Video saved: {output_path} ({size_mb:.1f} MB)")
    else:
        print("✗ No frames captured")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record robot LLM demo as high-FPS video")
    parser.add_argument("--output", default="robot_llm.mp4", help="Output video file")
    parser.add_argument("--max-steps", type=int, default=50, help="Max LLM steps")
    parser.add_argument("--fps", type=int, default=60, help="Video FPS")
    parser.add_argument("--frames-per-step", type=int, default=20, help="Frames per tool call")
    parser.add_argument("--provider", default="openrouter", choices=["openrouter", "openai"], help="LLM provider")
    args = parser.parse_args()
    
    try:
        record_llm_video(
            args.output,
            args.max_steps,
            args.fps,
            args.frames_per_step,
            args.provider
        )
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
