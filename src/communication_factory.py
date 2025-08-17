from abstract_communication import AbstractCommunication
from ip_communication import IPCommunication

from crypto_factory import CryptoFactory
# Future protocols (LoRA, Bluetooth, etc.) can be added here.


class CommunicationFactory:
    @staticmethod
    def build_transport(kind: str) -> AbstractCommunication:
        """
        Factory function to return a communication handler
        based on the requested transport type.

        Every concrete communication class must derive from
        AbstractCommunication to guarantee a consistent API.

        Args:
            kind (str): Type of communication transport (e.g., TCP)

        Returns:
            AbstractCommunication: Concrete communication instance.
        """
        if kind == "TCP":
            return IPCommunication()
        elif kind == "LoRA":
            # Placeholder: actual LoRA implementation pending
            return IPCommunication()
        elif kind == "Bluetooth":
            # Placeholder: actual Bluetooth implementation pending
            return IPCommunication()
        else:
            raise ValueError(f'Unsupported transport type "{kind}"')


if __name__ == "__main__":
    try:
        tcp: AbstractCommunication = CommunicationFactory.build_transport("TCP")
        print("✅ TCP communication factory call succeeded")

        lora: AbstractCommunication = CommunicationFactory.build_transport("LoRA")
        print("✅ LoRA communication factory call succeeded (stub)")

        bt: AbstractCommunication = CommunicationFactory.build_transport("Bluetooth")
        print("✅ Bluetooth communication factory call succeeded (stub)")

        # This one should raise an error
        bad: AbstractCommunication = CommunicationFactory.build_transport("Magic")
    except ValueError as err:
        print(f"❌ Communication type error: {err}")
