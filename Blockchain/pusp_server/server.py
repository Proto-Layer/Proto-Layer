import asyncio
import json
from tcp_server.handlers import handle_request


async def handle_client(reader, writer):
    """
    Handles a single TCP client connection.

    Args:
        reader: asyncio StreamReader
        writer: asyncio StreamWriter
    """
    addr = writer.get_extra_info('peername')
    print(f"[+] Connected: {addr}")

    try:
        while True:
            line = await reader.readline()
            if not line:
                break
            try:
                request = json.loads(line.decode())
                response = await handle_request(request)
            except Exception as e:
                response = {"error": str(e)}

            writer.write((json.dumps(response) + "\n").encode())
            await writer.drain()
    finally:
        print(f"[-] Disconnected: {addr}")
        writer.close()
        await writer.wait_closed()


async def start_tcp_server(host="127.0.0.1", port=9000):
    """
    Starts the TCP server to handle incoming client connections.

    Args:
        host (str): Host to bind the server.
        port (int): Port to listen on.
    """
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"[TCP] Listening on {addr}")
    async with server:
        await server.serve_forever()
