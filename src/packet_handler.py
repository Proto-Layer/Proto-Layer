import struct
from logging import Logger
from typing import Optional
from datetime import datetime

from packet_generator import PacketType, PacketGenerator
from packet_utils import PacketUtils
from logger_util import setup_logger

logger: Logger = setup_logger('PacketHandler', 'packet_handler.log')


class PacketHandler:
    """
    Handles incoming packets, decodes them, and calls the appropriate handler.
    """

    def __init__(self, packet_generator: PacketGenerator) -> None:
        self.packet_generator: PacketGenerator = packet_generator
        self.handlers = {
            PacketType.VALIDATOR_REQUEST: self.handle_validator_request,
            PacketType.VALIDATOR_CONFIRMATION: self.handle_validator_confirmation,
            PacketType.VALIDATOR_STATE: self.handle_validator_state,
            PacketType.VALIDATOR_LIST_REQUEST: self.handle_validator_list_request,
            PacketType.VALIDATOR_LIST_RESPONSE: self.handle_validator_list_response,
            PacketType.LATENCY: self.handle_latency,
            PacketType.JOB_FILE: self.handle_job_file,
            PacketType.PAYOUT_FILE: self.handle_payout_file,
            PacketType.SHUT_UP: self.handle_shut_up,
            PacketType.CONVERGENCE: self.handle_convergence,
            PacketType.SYNC_CO_CHAIN: self.handle_sync_co_chain,
            PacketType.SHARE_RULES: self.handle_share_rules,
            PacketType.JOB_REQUEST: self.handle_job_request,
            PacketType.VALIDATOR_CHANGE_STATE: self.handle_validator_change_state,
            PacketType.REPORT: self.handle_report_packet,
            PacketType.PERCEPTION_UPDATE: self.handle_perception_update_packet,
        }

    def handle_packet(self, packet: bytes) -> Optional[bytes]:
        try:
            if len(packet) < 15:
                logger.error("Packet too short to handle.")
                return None

            version_data = struct.unpack('!HBBB', packet[:5])
            timestamp = struct.unpack('!Q', packet[5:13])[0]

            self.version_info = {
                "year": version_data[0],
                "month": version_data[1],
                "day": version_data[2],
                "sub_version": version_data[3],
                "timestamp": timestamp
            }

            human_readable_timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')
            logger.info(f"Packet version: {self.version_info}")
            logger.info(f"Packet timestamp: {human_readable_timestamp}")

            packet_type_value = struct.unpack('!H', packet[13:15])[0]
            packet_type = PacketType(packet_type_value)
            logger.info(f"Received packet of type: {packet_type.name}")
            logger.debug(f"Packet payload (hex, truncated): {packet[15:35].hex()}...")

            handler = self.handlers.get(packet_type)
            if handler:
                return handler(packet[15:])
            else:
                logger.error(f"Unknown packet type: {packet_type}")
                return None

        except Exception as e:
            logger.error(f"Failed to handle packet: {e}")
            return None

    def handle_validator_request(self, packet: bytes) -> Optional[bytes]:
        logger.info("Handling Validator Request")
        try:
            public_key = packet.decode("utf-8")
        except Exception as e:
            logger.error(f"Unable to extract the public key: {e}")
            return None

        logger.info(f"Validator request from: {public_key}")
        return self.packet_generator.generate_validator_confirmation(position_in_queue=4)

    def handle_validator_confirmation(self, packet: bytes) -> None:
        logger.info("Handling Validator Response")
        try:
            queue_position = struct.unpack(">I", packet[:4])[0]
            logger.info(f"Validator confirmed in queue position: {queue_position}")
        except Exception as e:
            logger.error(f"Failed to unpack confirmation packet: {e}")

    def handle_validator_state(self, packet: bytes) -> None:
        logger.info("Handling Validator State")
        state = packet[2:].decode("utf-8")
        logger.info(f"Validator state is: {state}")

    def handle_validator_list_request(self, packet: bytes) -> None:
        logger.info("Handling Validator List Request")
        include_hash, slice_index = struct.unpack(">BI", packet[2:7])
        logger.info(f"Validator List Request: Include Hash: {include_hash}, Slice Index: {slice_index}")

    def handle_validator_list_response(self, packet: bytes, slice_index: Optional[int] = None) -> None:
        logger.info("Handling Validator List Response")
        validators_data = packet[2:].decode("utf-8")
        validators = validators_data.split(",")
        if slice_index is not None:
            logger.info(f"Received validator slice at index {slice_index}: {validators}")
        else:
            logger.info(f"Received full validator list: {validators}")

    def handle_latency(self, packet: bytes) -> None:
        logger.info("Handling Latency Packet")
        latency_counter = struct.unpack(">I", packet[2:6])[0]
        logger.info(f"Latency Counter: {latency_counter}")

    def handle_job_file(self, packet: bytes) -> None:
        logger.info("Handling Job File")
        job_data = packet[2:]
        logger.info(f"Job File Data: {job_data.decode('utf-8')}")

    def handle_payout_file(self, packet: bytes) -> None:
        logger.info("Handling Payout File")
        payout_data = packet[2:]
        logger.info(f"Payout File Data: {payout_data.decode('utf-8')}")

    def handle_shut_up(self, packet: bytes) -> None:
        logger.info("Handling Shut-Up Packet")

    def handle_convergence(self, packet: bytes) -> None:
        logger.info("Handling Convergence Packet")
        convergence_time = struct.unpack(">I", packet[2:6])[0]
        logger.info(f"Convergence Time: {convergence_time}")

    def handle_sync_co_chain(self, packet: bytes) -> None:
        logger.info("Handling Sync Co-Chain Packet")
        co_chain_id = packet[2:].decode("utf-8")
        logger.info(f"Sync Co-Chain ID: {co_chain_id}")

    def handle_share_rules(self, packet: bytes) -> None:
        logger.info("Handling Share Rules Packet")
        rule_version = packet[2:].decode("utf-8")
        logger.info(f"Share Rules version: {rule_version}")

    def handle_job_request(self, packet: bytes) -> None:
        logger.info("Handling Job Request")
        job_data = packet[2:].decode("utf-8")
        logger.info(f"Job Request Data: {job_data}")

    def handle_validator_change_state(self, packet: bytes) -> None:
        logger.info("Handling Validator Change State")
        new_state = packet[2:].decode("utf-8")
        logger.info(f"Validator changed to state: {new_state}")

    def handle_report_packet(self, packet_data: bytearray) -> None:
        reporter = PacketUtils._decode_public_key(packet_data[:64])
        reported = PacketUtils._decode_public_key(packet_data[64:128])
        reason = PacketUtils._decode_string(packet_data[128:])
        logger.info(f"Received report from {reporter} about {reported} for reason: {reason}.")

    def handle_perception_update_packet(self, packet_data: bytearray) -> None:
        user_id = PacketUtils._decode_public_key(packet_data[:64])
        new_score = int.from_bytes(packet_data[64:68], byteorder='big')
        logger.info(f"Updating perception score for user {user_id} to {new_score}.")

    def get_packet_type(self, packet: bytes) -> PacketType:
        try:
            pack_type_value = struct.unpack(">H", packet[:2])[0]
            return PacketType(pack_type_value)
        except Exception as e:
            logger.error(f'Failed to extract packet type: {e}')
            raise ValueError(f'Unknown packet type from packet {e}')


if __name__ == "__main__":
    packet_generator = PacketGenerator("2024.10.09.1")
    handler = PacketHandler(packet_generator)

    public_key = b"validator_pub_key_12345"
    sample_packet: bytes = packet_generator.generate_validator_request(public_key)
    print(f'Sample Packet: {sample_packet}')

    return_packet = handler.handle_packet(sample_packet)
    print(f"Generated return packet: {return_packet}")

    if return_packet:
        handler.handle_packet(return_packet)
