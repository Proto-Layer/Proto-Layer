import os
import json

import global_vars
from structures.threads_metadata_handlers import (
    GenerationThreadMetadataHandler,
    ApprovementThreadMetadataHandler
)
from utils import sha256


def init_protochain():
    """Initialize ProtoLayer chain data and thread metadata."""

    # Ensure data directory exists
    if not os.path.isdir(global_vars.PROTOCHAIN_DATA_PATH):
        try:
            os.makedirs(global_vars.PROTOCHAIN_DATA_PATH, mode=0o755, exist_ok=True)
        except OSError as e:
            print(f"[ERROR] Could not create chain data directory: {e}")
            return

    # Load Generation Thread state
    gt_data = global_vars.DB_BLOCKS.get("GEN_THREAD")
    if gt_data:
        try:
            gt_obj = GenerationThreadMetadataHandler.from_dict(json.loads(gt_data))
            global_vars.GEN_THREAD_HANDLER = gt_obj
        except Exception as e:
            print(f"[WARN] Failed to load Generation Thread: {e}")
            return

    # Load Approvement Thread state
    at_data = global_vars.DB_APPROVEMENT_META.get("APPROVE_THREAD")
    if at_data:
        try:
            at_obj = ApprovementThreadMetadataHandler.from_dict(json.loads(at_data))
            if at_obj.Cache is None:
                at_obj.Cache = {}
            global_vars.APPROVEMENT_HANDLER.Handler = at_obj
        except Exception as e:
            print(f"[WARN] Failed to load Approvement Thread: {e}")
            return

    # Initialize from genesis if no valid core version
    if global_vars.APPROVEMENT_HANDLER.Handler.CoreMajorVersion == -1:
        apply_genesis_state()
        try:
            serialized = json.dumps(
                global_vars.APPROVEMENT_HANDLER.Handler.to_dict()
            )
            global_vars.DB_APPROVEMENT_META.put("APPROVE_THREAD", serialized)
        except Exception as e:
            print(f"[ERROR] Could not persist Approvement Thread: {e}")


def apply_genesis_state():
    """Apply the genesis state to the chain (stub)."""
    pass
