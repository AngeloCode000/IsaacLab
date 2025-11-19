# Configuration for the Open Mutt quadruped.

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

OpenMuttCfg = ArticulationCfg(
    # Place robot under the standard env namespace; let tasks clone it per env
    prim_path="/World/envs/env_.*/Robot",
    # Explicitly target the articulation root in the USD.
    # The V2 asset places the articulation under '/MASTER'.
    articulation_root_prim_path="/MASTER",

    spawn=sim_utils.UsdFileCfg(
        # Note: filename is case-sensitive; use the exact V2 variant present on disk.
        usd_path="/home/eppl/Downloads/OpenMuttURDF_Master_Revolute/openmutt_master_revolute_absSTAGEV2.usd",
        activate_contact_sensors=True,
        # Ensure the robot is simulated with gravity and not anchored to the world.
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            kinematic_enabled=False,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=12,
            solver_velocity_iteration_count=1,
            # Ensure the base is not fixed to the world so robot can fall
            fix_root_link=False,
        ),
    ),

    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.6),           # (x, y, z) raise base so feet clear terrain
        rot=(0.0, 0.0, 0.0, 1.0),  # rotate +90 deg about X to stand upright (quaternion)
        lin_vel=(0.0, 0.0, 0.0),
        ang_vel=(0.0, 0.0, 0.0),
        # Home pose from RViz screenshot, rounded to nearest 0.5 rad.
        joint_pos={
            "Body_Bearing_2_Revolute_25": 0.0,
            "Body_Bearing_1_Revolute_63": 0.0,
            "Body_Bearing_3_Revolute_64": 0.0,
            "Body_Bearing_4_Revolute_65": 0.0,
            "Cycloidal_Simplified_for_FEA_v1_2_Revolute_99": -1.0,
            "Cycloidal_Simplified_for_FEA_v1_3_Revolute_100": 1.0,
            "Cycloidal_Simplified_for_FEA_v1_4_4_2_Revolute_101": 1.0,
            "Cycloidal_Simplified_for_FEA_v1_4_2_Revolute_102": 1.0,
            "Leg_Shank_Bushing_2_1_Revolute_103": -1.5,
            "Leg_Shank_Bushing_2_Revolute_104": 1.0,
            "Leg_Shank_Bushing_1_Revolute_105": -1.5,
            "Leg_Shank_Bushing_2_1_1_Revolute_106": 1.5,
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
