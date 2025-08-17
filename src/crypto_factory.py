from typing import Any, Tuple
from crypto_handler import CryptoHandler
from ecdsa_handler import ECDSAHandler


class CryptoFactory:
    """
    A singleton-style cryptographic factory that wraps around whichever
    handler is currently active. By default, we start with ECDSA, but
    the handler can be swapped at runtime to support other algorithms
    later without changing client code.
    """

    # Default crypto handler instance
    _handler: CryptoHandler = ECDSAHandler()

    @staticmethod
    def use_handler(handler: CryptoHandler) -> None:
        """
        Swap out the active crypto handler.

        Args:
            handler (CryptoHandler): The new cryptographic backend to use.
        """
        CryptoFactory._handler = handler

    @staticmethod
    def active_handler() -> CryptoHandler:
        """
        Get the active crypto handler instance.

        Returns:
            CryptoHandler: Currently configured handler.
        """
        if CryptoFactory._handler is None:
            raise ValueError("No crypto handler set. Did you reset it elsewhere?")
        return CryptoFactory._handler

    # === Wrappers around crypto operations ===

    @staticmethod
    def generate_keys() -> Tuple[Any, Any]:
        """Generate a fresh private/public key pair."""
        return CryptoFactory.active_handler().generate_keys(
