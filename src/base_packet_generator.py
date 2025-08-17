"""
Every user type has a shared set of packet formats they will use 
to communicate over the network. This module centralizes those 
definitions to simplify debugging and consistency.

These represent user-initiated packets. Separate handlers manage
system or network-originated events.

NOTE: Some packet types may still need future expansion.
"""

import time
from enum import IntEnum
from typing import Optional

from packet_header import PacketHeader, UserType


class CommonPacket(IntEnum):
    """
    Defines standard packet identifiers.
    We can allocate up to 999 distinct packet kinds.
    """
    QUIET = 1            # Sent when peer is spamming / too noisy
    SIGN_OFF = 2         # Gracefully close session
    PING = 3             # Used to measure round-trip delay
    SCORE_REQUEST = 4    # Ask for peer’s reputation/perception score
    KEEPALIVE = 5        # Heartbeat packet to prevent idle timeout
    COMPLAINT = 6        # Report abuse/misbehavior to the network
    MESSAGE = 7          # Direct user-to-user message (up to 4KB)
    LOCK = 8             # User action: freeze account in case of compromise
    APPROVE = 9          # Authorizes a network operation with proof
    REJECT = 10          # Refuses a pending operation/transaction
    SYNC_TIME = 11       # Query current network timestamp


class PacketBuilder:
    def __init__(self, version: tuple[int, int, int, int], user: UserType):
        """
        Args:
            version (tuple): (year, month, day, sub_version)
            user (UserType): type of user creating packets
        """
        self.version = version
        self.user = user

    def _make_header(
        self,
        packet_kind: CommonPacket,
        timestamp: Optional[int] = None,
        require_ack: bool = False
    ) -> bytes:
        """
        Internal utility for constructing a full packet header.
        """
        if timestamp is None:
            timestamp = int(time.time())

        header = PacketHeader(
            version=self.version,
            timestamp=timestamp,
            packet_type=packet_kind,
            user_type=self.user,
            ack_requested=require_ack
        )
        return header.encode()

    def _encode_text(self, text: str, max_size: int, length_bytes: int = 1) -> bytes:
        """
        Encode a string to UTF-8 with a prefixed length.
        """
        data = text.encode("utf-8")[:max_size]
        return len(data).to_bytes(length_bytes, "big") + data

    # --- Specific Packet Builders ---

    def quiet_notice(self) -> bytes:
        return self._make_header(CommonPacket.QUIET)

    def sign_off(self) -> bytes:
        return self._make_header(CommonPacket.SIGN_OFF)

    def latency_probe(self, sequence: int) -> bytes:
        header = self._make_header(CommonPacket.PING)
        return header + sequence.to_bytes(4, "big")

    def request_score(self) -> bytes:
        return self._make_h
