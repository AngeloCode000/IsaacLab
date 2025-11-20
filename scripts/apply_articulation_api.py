#!/usr/bin/env python3
"""
Apply USD Physics ArticulationRootAPI to a prim in a USD file.

Usage:
  Use the hardcoded defaults below or pass a different USD/prim via env vars.

Environment variables:
  USD_PATH   - path to the USD file to modify
  PRIM_PATH  - prim path to apply the API on (e.g., /MASTER)
"""

import os
import shutil
import sys

from pxr import Usd, UsdPhysics


def main():
    usd_path = os.environ.get(
        "USD_PATH",
        "/home/eppl/Downloads/OpenMuttURDF_Master_Revolute/openmutt_master_revolute_absSTAGEV2.usd",
    )
    prim_path = os.environ.get("PRIM_PATH", "/MASTER")

    if not os.path.isfile(usd_path):
        print(f"[ERROR] USD not found: {usd_path}")
        sys.exit(1)

    backup_path = usd_path + ".bak"
    try:
        shutil.copy2(usd_path, backup_path)
        print(f"[INFO] Backup created: {backup_path}")
    except Exception as e:
        print(f"[WARN] Could not create backup: {e}")

    stage = Usd.Stage.Open(usd_path)
    if stage is None:
        print(f"[ERROR] Failed to open USD stage: {usd_path}")
        sys.exit(2)

    prim = stage.GetPrimAtPath(prim_path)
    if not prim or not prim.IsValid():
        print(f"[ERROR] Prim not found or invalid at path: {prim_path}")
        sys.exit(3)

    # Apply the API if not already present
    already = bool(UsdPhysics.ArticulationRootAPI(prim))
    if not already:
        UsdPhysics.ArticulationRootAPI.Apply(prim)
        print(f"[INFO] Applied ArticulationRootAPI to {prim_path}")
    else:
        print(f"[INFO] ArticulationRootAPI already present on {prim_path}")

    # Persist changes
    stage.GetRootLayer().Save()
    print(f"[INFO] Saved USD: {usd_path}")


if __name__ == "__main__":
    main()

