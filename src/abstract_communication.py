from abc import ABC, abstractmethod

class BaseCommunication(ABC):
    """
    This abstract class provides a blueprint for implementing 
    different communication mechanisms. It defines the 
    essential operations: establishing connections, 
    listening, sending, receiving, and disconnecting.
    """

    @abstractmethod
    async def connect(self, target: bytearray, path: dict) -> None:
        """
        Open a connection to a target endpoint using the given path details.
        """
        pass

    @abstractmethod
    async def start_listener(self, host: str, port: int) -> None:
        """
        Begin listening for new connection requests on the provided host/port.
        """
        pass

    @abstractmethod
    async def send_message(self, data: bytes, target: bytearray) -> None:
        """
        Deliver a message (in bytes) to the specified target.
        """
        pass

    @abstractmethod
    async def receive_message(self, buffer_size: int = 1024) -> bytes:
        """
        Wait for and return a message from the active connection.
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """
        Terminate the active connection.
        """
        pass
