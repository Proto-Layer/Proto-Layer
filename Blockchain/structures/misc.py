from dataclasses import dataclass

@dataclass
class QuorumNode:
    """Represents a single member of the quorum with public key and endpoint URL."""
    pub_key: str
    endpoint: str
