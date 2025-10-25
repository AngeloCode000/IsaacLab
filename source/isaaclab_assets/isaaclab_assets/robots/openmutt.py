# Configuration for the Open Mutt quadruped.

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

OpenMuttCfg = ArticulationCfg(
    # This is where the robot will live in the stage at runtime. Keep it consistent with the USD.
    prim_path="/World/MASTER",

    spawn=sim_utils.UsdFileCfg(
        usd_path="/home/eppl/Downloads/openMutt_IsaacLab/configuration/OpenMuttMasterStage.usd",
        activate_contact_sensors=True,
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=12,
            solver_velocity_iteration_count=1,
        ),
    ),

    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.20),           # (x, y, z)
        rot=(1.0, 0.0, 0.0, 0.0),       # quaternion (w, x, y, z)
        lin_vel=(0.0, 0.0, 0.0),
        ang_vel=(0.0, 0.0, 0.0),
        # Zero pose to start—adjust if you have a “home” posture.
        joint_pos={
            "Body_Bearing_1_Revolute_63": 0.0,
            "Body_Bearing_2_Revolute_25": 0.0,
            "Body_Bearing_3_Revolute_64": 0.0,
            "Body_Bearing_4_Revolute_65": 0.0,
            "Cycloidal_Simplified_for_FEA_v1_2_Revolute_99": 0.0,
            "Cycloidal_Simplified_for_FEA_v1_3_Revolute_100": 0.0,
            "Cycloidal_Simplified_for_FEA_v1_4_2_Revolute_102": 0.0,
            "Cycloidal_Simplified_for_FEA_v1_4_4_2_Revolute_101": 0.0,
            "Leg_Shank_Bushing_1_Revolute_105": 0.0,
            "Leg_Shank_Bushing_2_1_1_Revolute_106": 0.0,
            "Leg_Shank_Bushing_2_1_Revolute_103": 0.0,
            "Leg_Shank_Bushing_2_Revolute_104": 0.0,
        },
        joint_vel={".*": 0.0},
    ),

actuators={
    "all_actuated": ImplicitActuatorCfg(
        # NOTE: use joint_names_expr (regex). Exact-name match: wrap with ^...$
        joint_names_expr=[
            r"^Body_Bearing_1_Revolute_63$",
            r"^Body_Bearing_2_Revolute_25$",
            r"^Body_Bearing_3_Revolute_64$",
            r"^Body_Bearing_4_Revolute_65$",
            r"^Cycloidal_Simplified_for_FEA_v1_2_Revolute_99$",
            r"^Cycloidal_Simplified_for_FEA_v1_3_Revolute_100$",
            r"^Cycloidal_Simplified_for_FEA_v1_4_2_Revolute_102$",
            r"^Cycloidal_Simplified_for_FEA_v1_4_4_2_Revolute_101$",
            r"^Leg_Shank_Bushing_1_Revolute_105$",
            r"^Leg_Shank_Bushing_2_1_1_Revolute_106$",
            r"^Leg_Shank_Bushing_2_1_Revolute_103$",
            r"^Leg_Shank_Bushing_2_Revolute_104$",
        ],
        stiffness=600.0,
        damping=30.0,
        effort_limit=None,
        velocity_limit=None,
    ),
}

)
