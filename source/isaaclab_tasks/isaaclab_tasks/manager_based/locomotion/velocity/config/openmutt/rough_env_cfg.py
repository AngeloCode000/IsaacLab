# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import math

from isaaclab.utils import configclass
from isaaclab.managers import SceneEntityCfg

from isaaclab_tasks.manager_based.locomotion.velocity.velocity_env_cfg import LocomotionVelocityRoughEnvCfg

##
# Pre-defined configs
##
from isaaclab_assets.robots.openmutt import OpenMuttCfg  # isort: skip


@configclass
class OpenMuttRoughEnvCfg(LocomotionVelocityRoughEnvCfg):
    """Rough-terrain locomotion environment configured for the OpenMutt quadruped."""

    def __post_init__(self):
        super().__post_init__()

        # swap in the OpenMutt articulation and map it to the environment namespace
        self.scene.robot = OpenMuttCfg.replace(prim_path="{ENV_REGEX_NS}/Robot")
        # Provide a nominal base height for rewards (matches OpenMutt target stance).
        self.default_base_height = 0.55

        # align sensor attachments with the robot's base link
        if self.scene.height_scanner is not None:
            self.scene.height_scanner.prim_path = "{ENV_REGEX_NS}/Robot/MASTER/base_link"
        if self.scene.contact_forces is not None:
            self.scene.contact_forces.prim_path = (
                "{ENV_REGEX_NS}/Robot/MASTER/(base_link|Leg_.*|SD_.*|Cycloidal_.*|Body_.*)"
            )

        # softer actions while bringing up a new robot
        self.actions.joint_pos.scale = 0.2

        # disable aggressive disturbances until the robot is tuned
        self.events.push_robot = None
        self.events.add_base_mass = None
        self.events.base_com = None
        self.events.base_external_force_torque = None

        # tighten the default reset ranges to keep the robot near nominal pose
        self.events.reset_base.params = {
            "pose_range": {"x": (-0.1, 0.1), "y": (-0.1, 0.1), "yaw": (-0.5, 0.5)},
            "velocity_range": {
                "x": (0.0, 0.0),
                "y": (0.0, 0.0),
                "z": (0.0, 0.0),
                "roll": (0.0, 0.0),
                "pitch": (0.0, 0.0),
                "yaw": (0.0, 0.0),
            },
        }
        self.events.reset_robot_joints.params["position_range"] = (0.8, 1.2)

        # disable rewards that rely on foot labels we don't have yet
        self.rewards.feet_air_time = None
        self.rewards.undesired_contacts = None

        # relax torque penalty until actuator gains are tuned
        self.rewards.dof_torques_l2.weight = -1.0e-4

        # base-contact termination now tracks the base_link body
        if self.terminations.base_contact is not None:
            self.terminations.base_contact.params["sensor_cfg"] = SceneEntityCfg(
                "contact_forces", body_names="base_link"
            )

        # With corrected USD (+X forward), no command-frame shim is required.


@configclass
class OpenMuttRoughEnvCfg_PLAY(OpenMuttRoughEnvCfg):
    """Lightweight configuration for quick visual checks."""

    def __post_init__(self):
        super().__post_init__()

        # shrink the scene for interactive play-throughs
        self.scene.num_envs = 16
        self.scene.env_spacing = 2.5
        self.scene.terrain.max_init_terrain_level = None
        if self.scene.terrain.terrain_generator is not None:
            self.scene.terrain.terrain_generator.num_rows = 4
            self.scene.terrain.terrain_generator.num_cols = 4
            self.scene.terrain.terrain_generator.curriculum = False

        # deterministic observations during manual testing
        if hasattr(self.observations, "policy"):
            self.observations.policy.enable_corruption = False
