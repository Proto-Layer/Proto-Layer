import struct
import time
from enum import Enum
from packet_utils import PacketUtils


class PacketType(Enum):
    VALIDATOR_REQUEST = 1
    VALIDATOR_CONFIRMATION = 2
    VALIDATOR_STATE = 3
    VALIDATOR_LIST_REQUEST = 4
    VALIDATOR_LIST_RESPONSE = 5
    JOB_FILE = 6
    PAYOUT_FILE = 7
    SHUT_UP = 8
    LATENCY = 9
    CONVERGENCE = 10
    SYNC_CO_CHAIN = 11
    SHARE_RULES = 12
    JOB_REQUEST = 13
    VALIDATOR_CHANGE_STATE = 14
    VALIDATOR_VOTE = 15
    RETURN_ADDRESS = 16
    REPORT = 17
    PERCEPTION_UPDATE = 18


class PacketGenerator:
    def __init__(self, version: str) -> None:
        """
        Version format: 'YYYY.MM.DD.subversion'.
        Stored as a tuple of integers for header generation.
        """
        self.version: tuple[int, int, int, int] = self._parse_version(version)

    def _parse_version(self, version: str) -> tuple[int, int, int, int]:
        year, month, day, sub_version = map(int, version.split('.'))
        return year, month, day, sub_version

    def _generate_header(self, packet_type: PacketType) -> bytes:
        """
        Header format:
        - Version: 16-bit year, 8-bit month, 8-bit day, 8-bit subversion
        - Timestamp: 64-bit UNIX timestamp
        - Packet Type: 16-bit integer
        """
        year, month, day, sub_version = self.version
        version_bytes = struct.pack('!HBBB', year, month, day, sub_version)
        timestamp_bytes = struct.pack('!Q', int(time.time()))
        packet_type_bytes = struct.pack('!H', packet_type.value)
        return version_bytes + timestamp_bytes + packet_type_bytes

    def generate_validator_request(self, public_key: bytes) -> bytes:
        header = self._generate_header(PacketType.VALIDATOR_REQUEST)
        payload = struct.pack(f'!{len(public_key)}s', public_key)
        return header + payload

    def generate_validator_confirmation(self, position_in_queue: int) -> bytes:
        header = self._generate_header(PacketType.VALIDATOR_CONFIRMATION)
        payload = struct.pack('!I', position_in_queue)
        return header + payload

    def generate_validator_state(self, state: str) -> bytes:
        header = self._generate_header(PacketType.VALIDATOR_STATE)
        encoded = state.encode('utf-8')
        payload = struct.pack(f'!{len(encoded)}s', encoded)
        return header + payload

    def generate_validator_list_request(self, include_hash: bool = False, slice_index: int = 0) -> bytes:
        header = self._generate_header(PacketType.VALIDATOR_LIST_REQUEST)
        payload = struct.pack('!BI', int(include_hash), slice_index)
        return header + payload

    def generate_validator_list_response(self, validator_list: list[bytes]) -> bytes:
        header = self._generate_header(PacketType.VALIDATOR_LIST_RESPONSE)
        payload = struct.pack('!I', len(validator_list))
        for validator in validator_list:
            payload += struct.pack(f'!{len(validator)}s', validator)
        return header + payload

    def generate_latency_packet(self, counter: int) -> bytes:
        header = self._generate_header(PacketType.LATENCY)
        payload = struct.pack('!I', counter)
        return header + payload

    def generate_job_file_packet(self, job_file_data: bytes) -> bytes:
        header = self._generate_header(PacketType.JOB_FILE)
        payload = struct.pack(f'!{len(job_file_data)}s', job_file_data)
        return header + payload

    def generate_payout_file_packet(self, payout_file_data: bytes) -> bytes:
        header = self._generate_header(PacketType.PAYOUT_FILE)
        payload = struct.pack(f'!{len(payout_file_data)}s', payout_file_data)
        return header + payload

    def generate_shut_up_packet(self) -> bytes:
        return self._generate_header(PacketType.SHUT_UP)

    def generate_convergence_packet(self, convergence_time: int) -> bytes:
        header = self._generate_header(PacketType.CONVERGENCE)
        payload = struct.pack('!I', convergence_time)
        return header + payload

    def generate_sync_co_chain_packet(self, co_chain_id: str, block_hash: str) -> bytes:
        header = self._generate_header(PacketType.SYNC_CO_CHAIN)
        co_bytes = co_chain_id.encode('utf-8')
        block_bytes = block_hash.encode('utf-8')
        payload = struct.pack(f'!{len(co_bytes)}s{len(block_bytes)}s', co_bytes, block_bytes)
        return header + payload

    def generate_share_rules_packet(self, rules_version: str) -> bytes:
        header = self._generate_header(PacketType.SHARE_RULES)
        payload = struct.pack(f'!{len(rules_version.encode("utf-8"))}s', rules_version.encode('utf-8'))
        return header + payload

    def generate_job_request_packet(self, job_request_data: bytes) -> bytes:
        header = self._generate_header(PacketType.JOB_REQUEST)
        payload = struct.pack(f'!{len(job_request_data)}s', job_request_data)
        return header + payload

    def generate_validator_change_state_packet(self, new_state: str) -> bytes:
        header = self._generate_header(PacketType.VALIDATOR_CHANGE_STATE)
        payload = struct.pack(f'!{len(new_state.encode("utf-8"))}s', new_state.encode('utf-8'))
        return header + payload

    def generate_validator_vote_packet(self, validator_id: str) -> bytes:
        header = self._generate_header(PacketType.VALIDATOR_VOTE)
        payload = struct.pack(f'!{len(validator_id.encode("utf-8"))}s', validator_id.encode('utf-8'))
        return header + payload

    def generate_return_address_packet(self, public_ip: str, public_port: int) -> bytes:
        header = self._generate_header(PacketType.RETURN_ADDRESS)
        payload = struct.pack(f'!{len(public_ip.encode("utf-8"))}sI', public_ip.encode('utf-8'), public_port)
        return header + payload

    def generate_report_packet(self, reporter: str, reported: str, reason: str) -> bytes:
        packet = bytearray()
        packet.extend(PacketUtils._encode_version("2024.08.12.1"))
        packet.extend(PacketUtils._encode_timestamp())
        packet.extend(PacketUtils._encode_public_key(reporter))
        packet.extend(PacketUtils._encode_public_key(reported))
        packet.extend(PacketUtils._encode_string(reason))
        packet_type_bytes = PacketType.REPORT.value.to_bytes(2, byteorder='big')
        return packet_type_bytes + packet

    def generate_perception_update_packet(self, user_id: str, new_score: int) -> bytes:
        packet = bytearray()
        packet.extend(PacketUtils._encode_version("2024.09.15.1"))
        packet.extend(PacketUtils._encode_timestamp())
        packet.extend(PacketUtils._encode_public_key(user_id))
        packet.extend(new_score.to_bytes(4, byteorder='big'))
        packet_type_bytes = PacketType.PERCEPTION_UPDATE.value.to_bytes(2, byteorder='big')
        return packet_type_bytes + packet


# Example test function
def test_packet_generator():
    generator = PacketGenerator("2024.08.30.1")

    pk = b"validator_pub_key"
    print("Validator Request Packet:", generator.generate_validator_request(pk).hex())
    print("Validator Confirmation Packet:", generator.generate_validator_confirmation(1).hex())
    print("Validator State Packet:", generator.generate_validator_state("ACTIVE").hex())
    print("Latency Packet:", generator.generate_latency_packet(12345).hex())
    print("Shut-Up Packet:", generator.generate_shut_up_packet().hex())


if __name__ == "__main__":
    test_packet_generator()
