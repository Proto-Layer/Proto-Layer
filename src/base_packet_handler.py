"""
This class complements the packet builder by defining how to process 
incoming packets. While the builder creates user-driven requests, 
this handler reacts to network-delivered events.
"""

from logging import Logger
from logger_util import setup_logger

log: Logger = setup_logger("PacketHandler", f"{__name__}.log")

from base_packet_generator import CommonPacket
from packet_header import PacketHeader


class PacketHandler:
    def __init__(self) -> None:
        # Map packet types to their respective handling functions
        self.routes = {
            CommonPacket.QUIET: self._on_quiet,
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
            packet_type = CommonPacket(header.packet_type)
        except ValueError:
            log.warning(f"Unrecognized packet type: {header.packet_type}")
            return

        handler = self.routes.get(packet_type)
        if handler is None:
            log.warning(f"No handler assigned for: {packet_type}")
            return

        handler(header, payload)

    # --- Individual Handlers ---
    def _on_quiet(self, header: PacketHeader, payload: bytes) -> None:
        print(f"[QUIET] signal received from {header.user_type_name}")
