import asyncio
from ip_communication import IPCommunication, MessageType


async def run_client() -> None:
    """
    Simple test client using IPCommunication.
    Connects to a target, sends a request, waits for reply, then disconnects.
    """
    comm = IPCommunication(version="1.0", co_chain_ID="chain-123")
    target = "127.0.0.1:4444"

    # Open connection to recipient
    await comm.connect(target=target.encode("utf-8"))  # type: ignore

    # Build and send a RETURN_ADDRESS packet
    packet = comm.generate_packet(
        message="Requesting public address",
        message_type=MessageType.RETURN_ADDRESS,
    )
    await comm.send_message(packet, target, use_TCP=True)  # type: ignore

    # Wait for reply
    reply: bytes | None = await comm.receive_message(use_TCP=True)
    if reply:
        print(f"[CLIENT] Got reply: {reply.decode('utf-8')}")

    # Clean up connection
    comm.disconnect()


if __name__ == "__main__":
    asyncio.run(run_client())
