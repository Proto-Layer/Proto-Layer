import os
import hashlib
from pathlib import Path
from typing import Dict, Any
import toml

from kv_storage import SimpleSQLiteDB

from structures.transaction import Transaction
from structures.threads_metadata_handlers import (
    EpochHandler,
    ApprovementThreadMetadataHandler,
    GenerationThreadMetadataHandler
)


def hash_sha256(text: str) -> str:
    """Return the SHA-256 hex digest of the given string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_db_instance(db_label: str) -> SimpleSQLiteDB:
    """Resolve SQLite DB instance for the given label."""
    base_dir = os.environ.get("PROTOCHAIN_DATA", "")
    db_path = os.path.join(base_dir, f"{db_label}.db")
    return SimpleSQLiteDB(db_path)


# Base storage path
PROTOCHAIN_DATA: str = os.environ.get("PROTOCHAIN_DATA", "")

if not PROTOCHAIN_DATA:
    raise EnvironmentError("PROTOCHAIN_DATA environment variable is required but not set.")

genesis_file = os.path.join(PROTOCHAIN_DATA, "genesis.toml")
if not os.path.isfile(genesis_file):
    raise FileNotFoundError(f"Genesis configuration missing: {genesis_file}")

with open(genesis_file, "r") as f:
    GENESIS_CONFIG = toml.load(f)

# Core version
with open("version.txt", "r") as vf:
    CORE_VERSION_MAJOR: int = int(vf.read().strip())

# Runtime caches and config
TRANSACTION_POOL: Dict[str, Transaction] = {}
RUNTIME_CONFIG: Dict[str, Any] = {}

CACHE_STORE: Dict[str, Any] = {
    "APPROVEMENT_CACHE": {},           # type: Dict[str, Any]
    "FINALIZATION_CACHE": {},          # type: Dict[str, Dict[str, str]]
    "TEMP_SESSION": {}                 # type: Dict[str, Any]
}

# Generation thread handler
GEN_THREAD_HANDLER = GenerationThreadMetadataHandler(
    epoch_full_id=hash_sha256(
        "abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef" +
        GENESIS_CONFIG["NETWORK_ID"]
    ) + "#-1",
    prev_hash="abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef",
    next_index=0
)

# Approvement thread
