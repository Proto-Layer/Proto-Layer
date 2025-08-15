from dataclasses import dataclass, field
from typing import Dict

@dataclass
class FinalizationProof:
    """Holds a proof for a single block finalization."""
    prev_hash: str
    block_id: str
    block_hash: str
    signatures: Dict[str, str]


@dataclass
class EpochFinalizationProof:
    """Aggregated finalization proof across an epoch."""
    last_leader_index: int
    last_block_index: int
    last_block_hash: str
    first_block_hash_by_last_leader: str
    signatures: Dict[str, str]


@dataclass
class LeaderRotationProof:
    """Proof for leader rotation across blocks."""
    first_block_hash: str
    skip_index: int
    skip_hash: str
    signatures: Dict[str, str]


@dataclass
class VotingStat:
    """Tracks voting stats for a pool."""
    index: int = -1
    block_hash: str = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    afp: FinalizationProof = field(default_factory=lambda: FinalizationProof(
        prev_hash="",
        block_id="",
        block_hash="",
        signatures={}
    ))


def new_voting_stat() -> VotingStat:
    return VotingStat()


@dataclass
class AlrpTemplate:
    """Skeleton structure for ALRP data."""
    afp_for_first_block: FinalizationProof = field(default_factory=lambda: FinalizationProof("", "", "", {}))
    skip_data: VotingStat = field(default_factory=new_voting_stat)
    signatures: Dict[str, str] = field
