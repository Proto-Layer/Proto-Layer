import datetime

class PacketUtils:
    """
    Utility class to handle encoding and decoding of values 
    such as version, timestamps, public keys, and generic strings.
    """

    @staticmethod
    def _encode_version(version: str) -> bytearray:
        """
        Encodes a version string into a bytearray.
        Format: YYYY.MM.DD.subversion
        """
        year, month, day, subversion = version.split(".")
        return (
            int(year).to_bytes(2, byteorder='big') +
            int(month).to_bytes(1, byteorder='big') +
            int(day).to_bytes(1, byteorder='big') +
            int(subversion).to_bytes(2, byteorder='big')
        )

    @staticmethod
    def _decode_version(data: bytearray) -> str:
        """
        Decodes a version from a bytearray back to string format.
        """
        year = int.from_bytes(data[:2], byteorder='big')
        month = int.from_bytes(data[2:3], byteorder='big')
        day = int.from_bytes(data[3:4], byteorder='big')
        subversion = int.from_bytes(data[4:6], byteorder='big')
        return f"{year:04}.{month:02}.{day:02}.{subversion:04}"

    @staticmethod
    def _encode_timestamp() -> bytearray:
        """
        Encodes the current UTC timestamp into a bytearray (Unix time).
        """
        timestamp = int(datetime.datetime.utcnow().timestamp())
        return timestamp.to_bytes(4, byteorder='big')

    @staticmethod
    def _decode_timestamp(data: bytearray) -> str:
        """
        Decodes a timestamp from a bytearray into a readable ISO date/time string.
        """
        timestamp = int.from_bytes(data, byteorder='big')
        return datetime.datetime.utcfromtimestamp(timestamp).isoformat()

    @staticmethod
    def _encode_public_key(public_key: str) -> bytearray:
        """
        Encodes a public key string into a bytearray.
        """
        return bytearray(public_key, "utf-8")

    @staticmethod
    def _decode_public_key(data: bytearray) -> str:
        """
        Decodes a bytearray back into a public key string.
        """
        return data.decode("utf-8")

    @staticmethod
    def _encode_string(value: str) -> bytearray:
        """
        Encodes a generic string into a bytearray.
        """
        return bytearray(value, "utf-8")

    @staticmethod
    def _decode_string(data: bytearray) -> str:
        """
        Decodes a bytearray back into a string.
        """
        return data.decode("utf-8")
