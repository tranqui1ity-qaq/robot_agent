"""Environment wrapper for Panda Pick and Place task.

Provides a high-level macro-action controller for panda-gym so that
a LLM can issue discrete commands (move to position, open/close gripper)
instead of low-level continuous control.
"""

from typing import Dict, Union

import gymnasium as gym
import numpy as np
import panda_gym  # registers PandaPickAndPlace-v3 in gymnasium registry, not used directly


class RobotArmController:
    """High-level wrapper around PandaPickAndPlace-v3.

    Translates absolute end-effector targets and gripper commands into
    low-level panda-gym actions by internally looping env.step().
    """

    def __init__(self, render_mode: str = "human") -> None:
        """Initialize the environment and reset the simulation.

        Args:
            render_mode: Gymnasium render mode ("human" or "rgb_array").
        """
        self.env = gym.make("PandaPickAndPlace-v3", render_mode=render_mode)
        self._base_env = self.env.unwrapped
        self.obs: Dict[str, np.ndarray]
        self.info: Dict[str, Union[bool, float]]
        self.obs, self.info = self.env.reset()

        # Rough workspace limits in world coordinates (meters).
        self.workspace_bounds = {
            "x_min": -1.0,
            "x_max": 0.2,
            "y_min": -0.6,
            "y_max": 0.6,
            "z_min": 0.0,
            "z_max": 1.2,
        }
        self.position_tolerance = 0.01
        self.max_move_steps = 200
        self.gripper_steps = 30
        self.gripper_open_target = 0.08
        self.gripper_closed_target = 0.00

    def _is_in_workspace(self, pos: np.ndarray) -> bool:
        b = self.workspace_bounds
        return (
            b["x_min"] <= pos[0] <= b["x_max"]
            and b["y_min"] <= pos[1] <= b["y_max"]
            and b["z_min"] <= pos[2] <= b["z_max"]
        )

    def step_to_position(
        self, target_x: float, target_y: float, target_z: float
    ) -> str:
        """Move the end-effector to an absolute XYZ target.

        Internally computes delta commands and loops env.step() until
        the end-effector is within ``position_tolerance`` of the target.

        Args:
            target_x: Target X coordinate (world frame).
            target_y: Target Y coordinate (world frame).
            target_z: Target Z coordinate (world frame).

        Returns:
            Human-readable status string describing the result.
        """
        target = np.array([target_x, target_y, target_z], dtype=np.float32)

        if not self._is_in_workspace(target):
            return (
                f"Error: target {target.tolist()} is outside the robot workspace "
                f"({self.workspace_bounds}). Please choose a coordinate inside the workspace."
            )

        for _ in range(self.max_move_steps):
            current = self._base_env.robot.get_ee_position()
            delta = target - current
            if np.linalg.norm(delta) < self.position_tolerance:
                break

            # panda-gym: ee_displacement = action[:3] * 0.05
            action = np.zeros(4, dtype=np.float32)
            action[:3] = np.clip(delta / 0.05, -1.0, 1.0)
            action[3] = 0.0  # do not change gripper while moving
            self.obs, _, terminated, _, self.info = self.env.step(action)
            if terminated:
                break

        final_pos = self._base_env.robot.get_ee_position()
        dist = float(np.linalg.norm(target - final_pos))
        return (
            f"End-effector moved to approximately {final_pos.tolist()} "
            f"(distance to target: {dist:.4f} m)."
        )

    def control_gripper(self, open_gripper: bool, target_width: float | None = None) -> str:
        """Open or close the gripper while keeping the arm joints locked.

        Instead of sending ``action[:3]=0`` through ``env.step()`` (which causes
        IK re-computation and arm jitter), this method directly controls the
        finger joints via PyBullet ``POSITION_CONTROL`` while freezing the arm.

        Args:
            open_gripper: True to open, False to close.
            target_width: Optional exact target finger width. When ``None``,
                defaults to ``gripper_open_target`` (0.08 m) or
                ``gripper_closed_target`` (0.00 m).

        Returns:
            Human-readable status string.
        """
        if target_width is not None:
            width = target_width
        else:
            width = self.gripper_open_target if open_gripper else self.gripper_closed_target
        robot = self._base_env.robot
        sim = self._base_env.sim

        for _ in range(self.gripper_steps):
            current_width = robot.get_fingers_width()
            if abs(current_width - width) < 0.005:
                break
            if open_gripper and current_width > width:
                break
            if not open_gripper and current_width < width:
                break

            # Lock arm joints at their current values; move fingers only.
            current_angles = np.array(
                [sim.get_joint_angle(robot.body_name, j) for j in robot.joint_indices]
            )
            target_angles = current_angles.copy()
            target_angles[-2] = width / 2.0
            target_angles[-1] = width / 2.0

            sim.control_joints(
                body=robot.body_name,
                joints=robot.joint_indices,
                target_angles=target_angles,
                forces=robot.joint_forces,
            )
            sim.step()

        final_width = float(robot.get_fingers_width())
        state = "opened" if open_gripper else "closed"
        return f"Gripper {state} (width={final_width:.4f} m)."

    def get_observation(self) -> Dict[str, Union[list, float, bool]]:
        """Return a structured dictionary of the current scene state.

        Returns:
            Dictionary containing end-effector position, gripper width,
            object position, target (goal) position, and success flag.
        """
        return {
            "ee_position": self._base_env.robot.get_ee_position().astype(float).tolist(),
            "gripper_width": float(self._base_env.robot.get_fingers_width()),
            "object_position": self._base_env.sim.get_base_position("object")
            .astype(float)
            .tolist(),
            "target_position": self._base_env.task.get_goal().astype(float).tolist(),
            "success": bool(self.info.get("is_success", False)),
        }

    def close(self) -> None:
        """Close the underlying simulation."""
        self.env.close()


if __name__ == "__main__":
    # NOTE: Use "rgb_array" in headless/WSL-like environments. Switch to "human" on a desktop with WSLg/X11.
    print("Initializing RobotArmController (render_mode='rgb_array')...")
    controller = RobotArmController(render_mode="rgb_array")

    print("\nInitial observation:")
    print(controller.get_observation())

    # Raw observation layout: ee_pos(3), ee_vel(3), fingers_width(1),
    # object_pos(3), object_rot(3), object_vel(3), object_ang_vel(3)
    obj_pos = np.array(controller.obs["observation"][7:10])
    print(f"\nDetected object position: {obj_pos.tolist()}")

    # Move 10 cm above the object so the gripper does not collide prematurely
    above_obj = obj_pos.copy()
    above_obj[2] += 0.10
    print(f"Moving end-effector 10 cm above object -> {above_obj.tolist()}")
    result = controller.step_to_position(*above_obj)
    print(result)

    print("\nClosing gripper...")
    print(controller.control_gripper(open_gripper=False))

    print("\nFinal observation:")
    print(controller.get_observation())

    controller.close()
    print("\nTest finished successfully.")
