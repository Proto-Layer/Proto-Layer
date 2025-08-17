from abc import ABC, abstractmethod
from typing import Tuple, Any

class CryptoHandler(ABC):
    """
    Abstract base class for all cryptographic operations used by ProtoLayer.
    This structure allows ProtoLayer to switch cryptographic implementations
    without needing major code rewrites.
    """

    @abstractmethod
    def generate_keys(self) -> Tuple[Any, Any]:
        """
        Create a new pair of private and public keys.

        Returns:
            Tuple[Any, Any]: Generated private key and corresponding public key.
        """
        pass

    @abstractmethod
    def serialize_public_key(self, public_key: Any) -> str:
        """
        Convert a public key into PEM format for storage or transmission.

        Returns:
            str: The public key in PEM representation.
        """
        pass

    @abstractmethod
    def save_keys(self, private_key: Any, public_key: Any, file_name: str, directory: str = '.') -> str:
        """
        Persist both private and public keys to files. The private key is securely encrypted.

        Returns:
            str: A confirmation message with the location of the saved keys.
        """
        pass

    @abstractmethod
    def load_private_key(self, filepath: str, salt_filepath: str) -> Any:
        """
        Retrieve a private key from a PEM file using a salt for decryption.

        Returns:
            Any: The decrypted private key object.
        """
        pass

    @abstractmethod
    def load_public_key(self, filepath: str) -> Any:
        """
        Load a public key from a PEM file.

        Returns:
            Any: The public key object.
        """
        pass

    @abstractmethod
    def sign_message(self, private_key: Any, message: bytes) -> bytes:
        """
        Produce a digital signature for a message using a private key.

        Returns:
            bytes: Signature in byte format.
        """
        pass

    @abstractmethod
    def verify_signature(self, public_key: Any, message: bytes, signature: bytes) -> bool:
        """
        Confirm that a message was signed by the holder of the corresponding private key.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        pass

    @abstractmethod
    def symmetric_encrypt_message(self, public_key: Any, message: bytes) -> Tuple[bytes, bytes, bytes, bytes]:
        """
        Encrypt a message using AES symmetric encryption, keyed with the recipient's public key.

        Returns:
            Tuple[bytes, bytes, bytes, bytes]: Ciphertext, ephemeral public key, nonce, and authentication tag.
        """
        pass

    @abstractmethod
    def symmetric_decrypt_message(self, private_key: Any, cipher_text: bytes, ephemeral_public_key_bytes: bytes, nonce: bytes, tag: bytes) -> bytes:
        """
        Decrypt an AES-encrypted message using the recipient's private key.

        Returns:
            bytes: Original plaintext message.
        """
        pass

    @abstractmethod
    def derive_symmetric_key(self, private_key: Any, public_key: Any) -> bytes:
        """
        Generate a symmetric key derived from a shared secret exchange.

        Returns:
            bytes: The resulting symmetric key.
        """
        pass

    @abstractmethod
    def asymmetric_encrypt_message(self, public_key: Any, message: bytes) -> Tuple[bytes, bytes, bytes, bytes]:
        """
        Encrypt a message with asymmetric encryption using the recipient's public key.

        Returns:
            Tuple[bytes, bytes, bytes, bytes]: Encrypted message, ephemeral public key, nonce, and authentication tag.
        """
        pass

    @abstractmethod
    def asymmetric_decrypt_message(self, private_key: Any, encrypted_message: bytes, ephemeral_public_key_bytes: bytes, nonce: bytes, tag: bytes) -> bytes:
        """
        Decrypt a message encrypted via asymmetric cryptography using the private key.

        Returns:
            bytes: Decrypted message in bytes.
        """
        pass
