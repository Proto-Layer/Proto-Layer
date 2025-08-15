import hashlib
import time
from typing import List

from structures.threads_metadata_handlers import EpochHandler, ApprovementThreadMetadataHandler
from global_vars import CORE_VERSION_MAJOR
from structures.misc import QuorumMemberData


def hash_sha256(text: str) -> str:
    """Return SHA-256 hex digest for given text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def utc_millis() -> int:
    """Get current UTC timestamp in milliseconds."""
    return int(time.time() * 1000)


def core_version_outdated(approval_thread: ApprovementThreadMetadataHandler) -> bool:
    """Check if the thread's core version is newer than this node's."""
    return approval_thread.core_major_version > CORE_VERSION_MAJOR


def epoch_is_active(approval_thread: ApprovementThreadMetadataHandler) -> bool:
    """Check if the epoch is still within its defined lifespan."""
    return (
        approval_thread.epoch.start_timestamp
        + approval_thread.network_parameters.get("EPOCH_TIME", 0)
        > utc_millis()
    )


def calc_quorum_majority(approval_thread: ApprovementThreadMetadataHandler) -> int:
    """Calculate the majority count required for quorum."""
    size = len(approval_thread.epoch.quorum)
    required = (2 * size) // 3 + 1
    return size if required > size else required


def collect_quorum_info(approval_thread: ApprovementThreadMetadataHandler) -> List[QuorumMemberData]:
    """Get quorum member public keys and URLs."""
    members: List[QuorumMemberData] = []
    for pk in approval_thread.epoch.quorum:
        pool_data = read_from_approvement_state(f"{pk}(POOL)_STORAGE_POOL")
        members.append(QuorumMemberData(PubKey=pk, Url=pool_data.pool_url))
    return members


def read_from_approvement_state(validator_key: str):
    """Stub: Read validator state from Approvement Thread storage."""
    pass


def assign_leader_rotation(approval_thread: ApprovementThreadMetadataHandler, epoch_seed: str):
    """Stub: Assign leader sequence for the epoch."""
    pass


def current_epoch_members(epoch_handler: EpochHandler) -> List[str]:
    """Stub: Return current quorum member list."""
    pass
