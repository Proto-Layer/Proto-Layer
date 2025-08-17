from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.dh import DHPrivateKey
from cryptography.hmat.primitives.asymmetric.dsa import DSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x448 import X448PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hmat.backends import default_backend

import os
import getpass
from crypto_handler import CryptoHandler
from typing import Tuple

def generate_salt(length: int = 16) -> bytes:
    """
    Creates a random salt for securing private keys.

    Returns:
        bytes: The generated salt
    """
    return os.urandom(length)

class ECDSAHandler(CryptoHandler):
    """
    ECDSA implementation of the ProtoLayer CryptoHandler base class.
    """

    def __init__(self, curve: ec.EllipticCurve = ec.SECP521R1(), hash_algorithm=hashes.SHA512) -> None:
        """
        Initialize ECDSAHandler with the chosen elliptic curve and hash algorithm.
        """
        self.curve: ec.EllipticCurve = curve
        self.hash_algorithm = hash_algorithm

    def generate_keys(self) -> Tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
        """
        Create a new elliptic curve key pair.
        """
        private_key: ec.EllipticCurvePrivateKey = ec.generate_private_key(self.curve, default_backend())
        public_key: ec.EllipticCurvePublicKey = private_key.public_key()
        return private_key, public_key

    def serialize_public_key(self, public_key: ec.EllipticCurvePublicKey) -> str:
        """
        Convert the public key to PEM format.

        Returns:
            str: PEM-formatted public key
        """
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    def save_keys(self, private_key: ec.EllipticCurvePrivateKey, public_key: ec.EllipticCurvePublicKey, file_name: str, directory: str = '.') -> str:
        """
        Saves the private and public keys to PEM files. Encrypts the private key using a passphrase.

        Returns:
            str: Confirmation message
        """
        passphrase: bytes = getpass.getpass(prompt="Enter passphrase for private key encryption: ").encode()
        salt: bytes = generate_salt()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend()
        )
        key = kdf.derive(passphrase)

        encrypted_private_key: bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(key)
        )

        public_key_bytes: bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        private_key_path: str = f'{directory}\\{file_name}_private_key.PEM'
        with open(private_key_path, 'wb') as private_key_file:
            private_key_file.write(encrypted_private_key)

        public_key_path: str = f'{directory}\\{file_name}_public_key.PEM'
        with open(public_key_path, 'wb') as public_key_file:
            public_key_file.write(public_key_bytes)

        salt_path = f'{directory}\\{file_name}_salt.bin'
        with open(salt_path, 'wb') as salt_file:
            salt_file.write(salt)

        return f'{file_name} wallet keys saved successfully in {directory}'

    def load_private_key(self, filepath: str, salt_filepath: str) -> ec.EllipticCurvePrivateKey:
        """
        Load an encrypted private key from a PEM file.

        Returns:
            EllipticCurvePrivateKey: The loaded private key
        """
        passphrase: bytes = getpass.getpass(prompt='Enter passphrase for private key: ').encode()

        with open(salt_filepath, 'rb') as salt_file:
            salt = salt_file.read()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend()
        )
        key: bytes = kdf.derive(passphrase)

        with open(filepath, 'rb') as key_file:
            private_key: DHPrivateKey | Ed25519PrivateKey | Ed448PrivateKey | RSAPrivateKey | DSAPrivateKey | ec.EllipticCurvePrivateKey | X25519PrivateKey | X448PrivateKey = serialization.load_pem_private_key(
                key_file.read(),
                password=key,
                backend=default_backend()
            )
        return private_key  # type: ignore

    def load_public_key(self, filepath: str) -> ec.EllipticCurvePublicKey:
        """
        Load a public key from a PEM file.

        Returns:
            EllipticCurvePublicKey: Loaded public key
        """
        with open(filepath, 'rb') as key_file:
            return serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )  # type: ignore

    def sign_message(self, private_key: ec.EllipticCurvePrivateKey, message: bytes) -> bytes:
        """
        Sign a message using the private key.

        Returns:
            bytes: Signature
        """
        return private_key.sign(message, ec.ECDSA(self.hash_algorithm()))

    def verify_signature(self, public_key: ec.EllipticCurvePublicKey, message: bytes, signature: bytes) -> bool:
        """
        Verify that a message was signed with the corresponding private key.

        Returns:
            bool: True if signature is valid
        """
        try:
            public_key.verify(signature, message, ec.ECDSA(self.hash_algorithm()))
            return True
        except:
            return False

    def derive_symmetric_key(self, private_key: ec.EllipticCurvePrivateKey, public_key: ec.EllipticCurvePublicKey) -> bytes:
        """
        Generate a symmetric key from a shared secret via ECDH.

        Returns:
            bytes: Derived symmetric key
        """
        shared_secret = private_key.exchange(ec.ECDH(), public_key)
        return HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(shared_secret)

    def symmetric_encrypt_message(self, public_key: ec.EllipticCurvePublicKey, message: bytes) -> Tuple[bytes, bytes, bytes, bytes]:
        """
        Symmetric encryption using ECDH and AES-GCM.

        Returns:
            Tuple[bytes, bytes, bytes, bytes]: ciphertext, ephemeral public key, nonce, tag
        """
        ephemeral_private_key = ec.generate_private_key(public_key.curve, default_backend())
        ephemeral_public_key = ephemeral_private_key.public_key()
        derived_key = self.derive_symmetric_key(ephemeral_private_key, public_key)

        nonce = os.urandom(12)
        encryptor = Cipher(
            algorithms.AES(derived_key),
            modes.GCM(nonce),
            backend=default_backend()
        ).encryptor()
        ciphertext = encryptor.update(message) + encryptor.finalize()

        return ciphertext, ephemeral_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ), nonce, encryptor.tag

    def symmetric_decrypt_message(self, private_key: ec.EllipticCurvePrivateKey, cipher_text: bytes, ephemeral_public_key_bytes: bytes, nonce: bytes, tag: bytes) -> bytes:
        """
        Decrypt symmetric AES-GCM message using private key.

        Returns:
            bytes: Decrypted message
        """
        ephemeral_public_key = serialization.load_pem_public_key(ephemeral_public_key_bytes, backend=default_backend())
        derived_key = self.derive_symmetric_key(private_key, ephemeral_public_key)
        decryptor = Cipher(algorithms.AES(derived_key), modes.GCM(nonce, tag), backend=default_backend()).decryptor()
        return decryptor.update(cipher_text) + decryptor.finalize()

    def asymmetric_encrypt_message(self, public_key: ec.EllipticCurvePublicKey, message: bytes) -> Tuple[bytes, bytes, bytes, bytes]:
        """
        Encrypt a message asymmetrically using ECDH and AES-GCM.

        Returns:
            Tuple[bytes, bytes, bytes, bytes]: ciphertext, ephemeral public key, nonce, tag
        """
        ephemeral_private_key = ec.generate_private_key(public_key.curve, default_backend())
        ephemeral_public_key = ephemeral_private_key.public_key()
        shared_secret = ephemeral_private_key.exchange(ec.ECDH(), public_key)
        derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b
