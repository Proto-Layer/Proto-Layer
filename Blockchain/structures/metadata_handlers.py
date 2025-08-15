from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class EpochHandler:
    """Represents metadata about a single epoch."""
    id: int
    hash: str
    pools_registry: Dict[str, None]
    quorum: List[str]
    leaders_sequence: List[str]
    start_timestamp: int
    current_leader_index: int


@dataclass
class ApprovementThreadMetadataHandler:
    """Tracks the approvement thread state."""
    core_major_version: int
    network_parameters: Dict[str, Any]
    epoch: EpochHandler
    cache: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionThreadMetadataHandler:
    """Tracks execution thread state. Extra fields TBD."""
    core_major_version: int
    network_parameters: Dict[str, Any]
    epoch: EpochHandler
    cache: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerationThreadMetadataHandler:
    """Tracks generation thread state."""
    epoch_full_id: str
    prev_hash: str
    next_index: int
