"""OpenClaw-compatible robot skills for Panda Pick and Place.

This module exposes a set of high-level tool functions that a LLM/OpenClaw Agent
can reason about and call. Each function wraps the low-level :class:`env_wrapper.RobotArmController`
so that commands are executed as macro-actions in the :mod:`panda_gym` simulation.

Usage
-----
Simply import the functions and call them. The global controller is lazily-initialised
the first time any skill is invoked::

    from skills import perceive_environment, move_arm_to, grasp, release
    status = move_arm_to(0.1, 0.0, 0.5)
"""

from typing import Dict, List, Union

from env_wrapper import RobotArmController

# ---------------------------------------------------------------------------
# Global singleton – lazily initialised on first use so skills can be imported
# without spawning a simulation window immediately.
# ---------------------------------------------------------------------------
_controller: RobotArmController | None = None


def _ensure_initialized() -> RobotArmController:
    """Return the global controller, instantiating it if necessary.

    Returns:
        The shared :class:`env_wrapper.RobotArmController` instance.
    """
    global _controller
    if _controller is None:
        # "rgb_array" works in headless/WSL-like environments.
        # Change to "human" if you run on a desktop with WSLg / X11 / VcXsrv.
        _controller = RobotArmController(render_mode="rgb_array")
    return _controller


def perceive_environment() -> str:
    """Observe the scene and return a natural-language description.

    This gives the LLM everything it needs to plan the next action:
    end-effector pose, gripper aperture, cube location, and the
    (invisible green) target location.

    Returns:
        A human-readable summary of the current environment state.
        If the simulation has not been started yet, it is created first.
    """
    controller = _ensure_initialized()
    obs: Dict[str, Union[List[float], float, bool]] = controller.get_observation()

    ee = obs["ee_position"]  # type: ignore[index]
    obj = obs["object_position"]  # type: ignore[index]
    goal = obs["target_position"]  # type: ignore[index]
    fingers = obs["gripper_width"]  # type: ignore[index]
    success = obs["success"]  # type: ignore[index]

    return (
        f"Scene state:\n"
        f"  - End-effector:   ({ee[0]:+.3f}, {ee[1]:+.3f}, {ee[2]:+.3f})\n"
        f"  - Gripper width:  {fingers:.4f} m\n"
        f"  - Object (cube):  ({obj[0]:+.3f}, {obj[1]:+.3f}, {obj[2]:+.3f})\n"
        f"  - Target (goal):  ({goal[0]:+.3f}, {goal[1]:+.3f}, {goal[2]:+.3f})\n"
        f"  - Task success:   {success}"
    )


def move_arm_to(x: float, y: float, z: float) -> str:
    """Move the robot end-effector to an absolute (x, y, z) position in metres.

    The controller internally computes delta commands and loops
    :meth:`env.step` until the error is below a tolerance (≈1 cm).

    Args:
        x: Target X coordinate (world frame). Typical range: ~-1.0 … 0.2 m.
        y: Target Y coordinate (world frame). Typical range: ~-0.6 … 0.6 m.
        z: Target Z coordinate (world frame). Typical range: ~0.0 … 1.2 m.

    Returns:
        A status string describing whether the motion succeeded or, if the target
        lies outside the robot workspace, an error message that the LLM can use to
        self-correct.
    """
    controller = _ensure_initialized()
    try:
        return controller.step_to_position(x, y, z)
    except Exception as exc:  # pragma: no cover
        return f"Error during motion: {exc}. Please try again with a different coordinate."


def grasp() -> str:
    """Close the gripper to grasp the object.

    The gripper is closed to a width slightly smaller than the object
    (≈4 cm) so that the fingers are wedged against the cube. The arm is
    locked during finger motion to avoid disturbing the object.

    Returns:
        A status string confirming the new gripper width.
    """
    controller = _ensure_initialized()
    try:
        return controller.control_gripper(open_gripper=False, target_width=0.03)
    except Exception as exc:  # pragma: no cover
        return f"Error closing gripper: {exc}. Please try again."


def release() -> str:
    """Open the gripper to release the object.

    The function repeatedly steps the simulation until the fingers are
    nearly fully open.

    Returns:
        A status string confirming the new gripper width.
    """
    controller = _ensure_initialized()
    try:
        return controller.control_gripper(open_gripper=True)
    except Exception as exc:  # pragma: no cover
        return f"Error opening gripper: {exc}. Please try again."


def get_state_dict() -> Dict[str, Union[List[float], float, bool]]:
    """Return the raw structured observation dictionary.

    Useful for the demo policy or any downstream planner that needs numeric
    coordinates rather than a human-readable string.

    Returns:
        Dictionary with keys ``ee_position``, ``gripper_width``,
        ``object_position``, ``target_position``, ``success``.
    """
    controller = _ensure_initialized()
    return controller.get_observation()


def close_skills() -> str:
    """Shut down the robot controller and free the PyBullet / simulation resources.

    Call this when the episode (or program) ends so that the physics server
    disconnects gracefully.

    Returns:
        Confirmation string.
    """
    global _controller
    if _controller is not None:
        _controller.close()
        _controller = None
        return "Simulation closed successfully."
    return "No active simulation to close."


if __name__ == "__main__":
    # Minimal sanity check – runs the skills in a short toy sequence.
    print(perceive_environment())
    print()

    print("Opening gripper first...")
    print(release())
    print()

    # Move above the object (read from observation to pick a safe hover point)
    obs = _ensure_initialized().get_observation()
    obj = obs["object_position"]  # type: ignore[index]
    hover = [obj[0], obj[1], obj[2] + 0.10]
    print(f"Moving to hover point: {hover}")
    print(move_arm_to(*hover))
    print()

    print("Descending to grip height...")
    grip = [obj[0], obj[1], obj[2] + 0.03]
    print(move_arm_to(*grip))
    print(grasp())
    print()

    # Lift the cube
    lift = [obj[0], obj[1], obj[2] + 0.15]
    print(f"Lifting cube to: {lift}")
    print(move_arm_to(*lift))
    print()

    print(perceive_environment())
    print(close_skills())
