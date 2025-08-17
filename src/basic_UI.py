"""
This class complements the packet builder by defining how to process 
incoming packets. While the builder creates user-driven requests, 
this handler reacts to network-delivered events.
"""

from logging import Logger
from logger_util import setup_logger

log: Logger = setup_logger("PacketHandler", f"{__name__}.log")

from base_packet_generator import BasePacketType
from packet_header import PacketHeader


class PacketHandler:
    def __init__(self) -> None:
        # Map packet types to their respective handling functions
        self.routes = {
            BasePacketType.SHUT_UP: self._on_shut_up,
            BasePacketType.LOG_OFF: self._on_log_off,
            BasePacketType.LATENCY: self._on_latency,
            BasePacketType.REQUEST_SCORE: self._on_request_score,
            BasePacketType.HEARTBEAT: self._on_heartbeat,
            BasePacketType.REPORT: self._on_report,
            BasePacketType.DM: self._on_dm,
            BasePacketType.FREEZE: self._on_freeze,
            BasePacketType.AUTHORIZE: self._on_authorize,
            BasePacketType.DENY: self._on_deny,
            BasePacketType.TIMESTAMP: self._on_timestamp,
        }

    def process(self, raw_data: bytes) -> None:
        """
        Process an incoming packet. Attempts to parse a header; 
        if unsuccessful, assumes it may just be a raw payload.
        """
        header_length: int = PacketHeader.size()

        try:
            header: PacketHeader = PacketHeader.decode(raw_data[:header_length])
        except ValueError as err:
            log.error(f"[PacketHandler] Could not parse header: {err}")
            return

        payload: bytes = raw_data[header_length:]

        try:
            packet_type = BasePacketType(header.packet_type)
        except ValueError:
            log.warning(f"Unrecognized packet type: {header.packet_type}")
            return

        handler = self.routes.get(packet_type)
        if handler is None:
            log.warning(f"No handler assigned for: {packet_type}")
            return

        handler(header, payload)

    # --- Individual Handlers ---
    def _on_shut_up(self, header: PacketHeader, payload: bytes) -> None:
        print(f"[SHUT_UP] from {header.user_type_name}")

    def _on_log_off(self, header: PacketHeader, payload: bytes) -> None:
        print(f"[LOG_OFF] from {header.user_type_name}")

    def _on_latency(self, header: PacketHeader, payload: bytes) -> None:
        print(f"[LATENCY] probe from {header.user_type_name} (payload={payload})")

    def _on_request_score(self, header: PacketHeader, payload: bytes) -> None:
        print(f"[REQUEST_SCORE] from {header.user_type_name}")

    def _on_heartbeat(self, header: PacketHeader, payload: bytes) -> None:
        print(f"[HEARTBEAT] from {header.user_type_name}")

    def _on_report(self, header: PacketHeader, payload: bytes) -> None:
        print(f"[REPORT] from {header.user_type_name}, payload={payload}")

    def _on_dm(self, header: PacketHeader, payload: bytes) -> None:
        print(f"[DM] from {header.user_type_name}, message={payload}")

    def _on_freeze(self, header: PacketHeader, payload: bytes) -> None:
        print(f"[FREEZE] from {header.user_type_name}")

    def _on_authorize(self, header: PacketHeader, payload: bytes) -> None:
        print(f"[AUTHORIZE] from {header.user_type_name}, payload={payload}")

    def _on_deny(self, header: PacketHeader, payload: bytes) -> None:
        print(f"[DENY] from {header.user_type_name}, payload={payload}")

    def _on_timestamp(self, header: PacketHeader, payload: bytes) -> None:
        print(f"[TIMESTAMP] request from {header.user_type_name}")
