"""
SectorManager

Tracks per-sector state changes on a partner node between validator confirmations.
Monitors files in the sector, records all mutations, and allows reconstruction
of sector state at any given timestamp.

Critical for validating storage challenges and proving honest mutation handling
before a validator confirms the new Merkle root. After confirmation, old mutation
records can be cleared using commit_checkpoint() to save memory.
"""

import hashlib
from typing import List, Dict, Optional


class SectorManager:
    def __init__(self, sector_id: str, version: int = 1):
        self.sector_id = sector_id
        self.version = version
        self.files: Dict[str, str] = {}  # file_id -> mock content
        self.mutations: List[Dict] = []  # chronological mutations
        self.sector_size_limit = self.get_configured_sector_size()
        self.last_confirmed_root: Optional[str] = None

    def get_configured_sector_size(self) -> int:
        """Placeholder for sector size, replace with run rules config later."""
        return 4 * 1024 ** 3  # 4 GB

    # ----------------- Mutation Handling -----------------
    def apply_mutation(self, job: Dict) -> None:
        """
        Apply a mutation (write/update/delete) and log it in mutation history.
        Job must include: timestamp, user_pubkey, action, job_id, affected files.
        """
        required_fields = ["job_id", "timestamp", "user_pubkey", "action", "affected"]
        for field in required_fields:
            if field not in job:
                raise ValueError(f"Missing required field in job: {field}")

        for file_id in job["affected"]:
            if job["action"] in ("write", "update"):
                self.files[file_id] = f"data::{job['timestamp']}::{file_id}"
            elif job["action"] == "delete":
                self.files.pop(file_id, None)

        self.mutations.append(job)

    def get_state_at(self, timestamp: int) -> Dict[str, str]:
        """Reconstruct sector state at a given timestamp by replaying mutations."""
        state: Dict[str, str] = {}
        for job in sorted(self.mutations, key=lambda x: x["timestamp"]):
            if job["timestamp"] > timestamp:
                break
            for file_id in job["affected"]:
                if job["action"] in ("write", "update"):
                    state[file_id] = f"data::{job['timestamp']}::{file_id}"
                elif job["action"] == "delete":
                    state.pop(file_id, None)
        return state

    # ----------------- Merkle Root -----------------
    def calculate_merkle_root(self, state: Optional[Dict[str, str]] = None) -> str:
        """
        Compute a simulated Merkle root by hashing sorted file:content pairs.
        Placeholder for tree-based implementation.
        """
        if state is None:
            state = self.files
        flat = "".join(f"{k}:{v}" for k, v in sorted(state.items()))
        return hashlib.sha256(flat.encode()).hexdigest()

    # ----------------- Checkpointing -----------------
    def commit_checkpoint(self, root_hash: str, confirmed_time: int) -> None:
        """
        Confirm that all mutations up to 'confirmed_time' are permanent.
        Clears older mutations to reduce memory footprint.
        """
        self.last_confirmed_root = root_hash
        self.mutations = [m for m in self.mutations if m["timestamp"] > confirmed_time]


# ----------------- Example Usage -----------------
if __name__ == "__main__":
    import pprint

    sm = SectorManager(sector_id="sector_001")

    # Sample jobs
    jobs = [
        {"job_id": "job-001", "timestamp": 1723451000, "user_pubkey": "0xBOB", "action": "write", "affected": ["bob_notes.txt"]},
        {"job_id": "job-002", "timestamp": 1723451100, "user_pubkey": "0xSALLY", "action": "write", "affected": ["sally_resume.pdf"]},
        {"job_id": "job-003", "timestamp": 1723451200, "user_pubkey": "0xBOB", "action": "update", "affected": ["bob_notes.txt"]},
        {"job_id": "job-004", "timestamp": 1723451300, "user_pubkey": "0xSALLY", "action": "delete", "affected": ["sally_resume.pdf"]}
    ]

    for job in jobs:
        sm.apply_mutation(job)

    print("\n--- Current Sector State ---")
    pprint.pprint(sm.files)

    print("\n--- Mutation Log ---")
    pprint.pprint(sm.mutations)

    current_root = sm.calculate_merkle_root()
    print(f"\nMerkle Root (Current): {current_root}")

    ts_challenge = 1723451250
    snapshot = sm.get_state_at(ts_challenge)
    print(f"\n--- Reconstructed State @ {ts_challenge} ---")
    pprint.pprint(snapshot)

    snapshot_root = sm.calculate_merkle_root(snapshot)
    print(f"\nMerkle Root (Snapshot @ {ts_challenge}): {snapshot_root}")

    sm.commit_checkpoint(snapshot_root, confirmed_time=ts_challenge)
    print("\n--- Remaining Mutations After Commit ---")
    pprint.pprint(sm.mutations)

    print(f"\nMerkle Root (Post-Commit): {sm.calculate_merkle_root()}")
