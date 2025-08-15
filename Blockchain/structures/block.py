import json
import hashlib
import time
from dataclasses import dataclass
from typing import Dict, List

from proofs import AggregatedLeaderRotationProof, AggregatedEpochFinalizationProof
from transaction import Transaction


def utc_millis() -> int:
    """Return current UTC time in milliseconds."""
    return int(time.time() * 1000)


def sign_message(priv_key: str, payload: str) -> str:
    """Stub: Generate a signature for a given payload using a private key."""
    return f"sig({payload[:10]}...)"


def check_signature(payload: str, pub_key: str, sig: str) -> bool:
    """Stub: Verify that the given signature matches the payload and public key."""
    return sig.startswith("sig(")


@dataclass
class DeferredTransactions:
    """A set of delayed transactions along with their epoch and proofs."""
    epoch_idx: int
    txs: List[Dict[str, str]]
    proof_bundle: Dict[str, str]


@dataclass
class BlockExtra:
    """Holds auxiliary data attached to a block."""
    metadata: Dict[str, str]
    prev_epoch_finalization: A
