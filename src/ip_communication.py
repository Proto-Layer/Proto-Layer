import socket
import asyncio
from logging import Logger
from typing import Optional
from abstract_communication import AbstractCommunication
from logger_util import setup_logger

logger: Logger = setup_logger('IPCommunication', 'ip_communication.log')

class IPCommunication(AbstractCommunication):
    active_connections = 0

    def __init__(self) -> None:
        self.socket = None
        self.listener_socket = None
        self.listener_task = None

    async def connect(self, recipient: bytearray, route: dict) -> None:
        method = route.get('method', 'TCP')
        ip_address = route.get('ip')
        port = route.get('port')

        if not ip_address or not port:
            raise ValueError("IP address and port must be provided.")

        if method == 'TCP':
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            await asyncio.get_event_loop().sock_connect(self.socket, (ip_address, port))
            logger.info(f'Connected to {ip_address}:{port} via TCP')
        elif method == 'UDP':
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            logger.info(f'Using UDP for communication with {ip_address}:{port}')
        else:
            raise ValueError(f"Unsupported communication method: {method}")

    async def start_listener(self, host: str, port: int) -> None:
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.listener_socket.bind((host, port))
            self.listener_socket.listen(100)
            self.listener_socket.setblocking(False)
            logger.info(f'Listening on {host}:{port}')
            self.listener_task = asyncio.create_task(self.accept_connections())
            await self.listener_task
        except Exception as e:
            logger.error(f'Failed to start listener on {host}:{port}: {e}')
        finally:
            if self.listener_socket:
                self.listener_socket.close()
                logger.info('Listener socket closed')

    async def accept_connections(self) -> None:
        try:
            while True:
                user_socket, user_address = await asyncio.get_event_loop().sock_accept(self.listener_socket)  # type: ignore
                IPCommunication.active_connections += 1
                logger.info(f'Accepted connection from {user_address}. Active connections {IPCommunication.active_connections}')
                asyncio.create_task(self.handle_user(user_socket))
        except asyncio.CancelledError:
            logger.info("Listener task was cancelled, stopping accepting new connections.")
        except Exception as e:
            logger.error(f"Error in accepting connections: {e}")
        finally:
            if self.listener_socket:
                self.listener_socket.close()

    async def send_message(self, message: bytearray, recipient: bytearray) -> None:
        if self.socket:
            await asyncio.get_event_loop().sock_sendall(self.socket, message)
            logger.info(f'Sent message to {recipient}')
        else:
            raise ConnectionError("No active connection to send the message.")

    async def receive_message(self, buffer_size: int = 1024) -> bytes:
        if self.socket:
            return await asyncio.get_event_loop().sock_recv(self.socket, buffer_size)
        else:
            raise ConnectionError("No active connection to receive the message.")

    async def disconnect(self) -> None:
        try:
            if self.listener_task:
                self.listener_task.cancel()
                logger.info("Attempting to stop the listener task...")
                try:
                    await self.listener_task
                    logger.info("Listener task was cancelled successfully.")
                except asyncio.CancelledError:
                    logger.info("Listener task was cancelled successfully.")
                except Exception as e:
                    logger.error(f"Failed to await listener task cancellation: {e}")

            if self.socket:
                self.socket.close()
                self.socket = None
                IPCommunication.active_connections -= 1
                logger.info(f"Disconnected from peer. Active connections: {IPCommunication.active_connections}")

            if self.listener_socket:
                self.listener_socket.close()
                self.listener_socket = None
                logger.info("Listener socket closed.")
        except Exception as e:
            logger.error(f"Failed to disconnect properly: {e}")

    async def handle_user(self, user_socket: socket.socket) -> None:
        try:
            while True:
                try:
                    message: bytes = await asyncio.get_event_loop().sock_recv(user_socket, 1024)
                    if not message:
                        logger.warning('No message received. Closing connection.')
                        break
                    logger.info(f'Received message from peer: {message.decode("utf-8")}')
                    response: Optional[bytes] = self.handle_message(message)
                    if response:
                        await asyncio.get_event_loop().sock_sendall(user_socket, response)
                    else:
                        logger.warning("No response generated for the message.")
                except ConnectionResetError:
                    logger.error('Connection was reset by the peer.')
                    break
                except Exception as e:
                    logger.error(f'Error handling user connection: {e}')
                    break
        finally:
            user_socket.close()
            logger.info('Connection with peer closed.')

    async def handle_udp(self) -> None:
        try:
            while True:
                data, addr = await asyncio.get_event_loop().sock_recvfrom(self.socket, 1024)  # type: ignore
                logger.info(f'Received UDP message from {addr}: {data.decode("utf-8")}')
                response: Optional[bytes] = self.handle_message(data)
                if response:
                    self.socket.sendto(response, addr)  # type: ignore
        except Exception as e:
            logger.error(f"Error handling UDP message: {e}")

    def handle_message(self, message: bytes) -> Optional[bytes]:
        try:
            message_str: str = message.decode('utf-8')
            logger.info(f'Interpreted message: {message_str}')
            return message_str.encode('utf-8')  # Echo
        except Exception as e:
            logger.error(f'Error processing message: {e}')
            return None

    def acknowledge_message(self, message: bytearray) -> bytearray:
        ack = bytearray(f"ACK-{hash(message)}", "utf-8")
        logger.info("Acknowledgment sent for message")
        return ack
