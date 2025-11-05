# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""
Flat-terrain configuration for the OpenMutt velocity-tracking task.
"""

from isaaclab.utils import configclass

from .rough_env_cfg import OpenMuttRoughEnvCfg


@configclass
class OpenMuttFlatEnvCfg(OpenMuttRoughEnvCfg):
    """Specialization of the OpenMutt locomotion task for planar terrain."""

    def __post_init__(self):
        super().__post_init__()

        # enforce a flat ground plane
        if self.scene.terrain is not None:
            self.scene.terrain.terrain_type = "plane"
            self.scene.terrain.terrain_generator = None
            self.scene.terrain.max_init_terrain_level = None

        # remove terrain-dependent sensing
        self.scene.height_scanner = None
        if hasattr(self.observations, "policy"):
            self.observations.policy.height_scan = None

        # disable terrain difficulty curriculum
        if hasattr(self.curriculum, "terrain_levels"):
            self.curriculum.terrain_levels = None


@configclass
class OpenMuttFlatEnvCfg_PLAY(OpenMuttFlatEnvCfg):
    """Lightweight configuration for quick visual checks on flat terrain."""

    def __post_init__(self):
        super().__post_init__()

        # shrink the scene for interactive play-throughs
        self.scene.num_envs = 16
        self.scene.env_spacing = 2.5

        # deterministic observations during manual testing
        if hasattr(self.observations, "policy"):
            self.observations.policy.enable_corruption = False
