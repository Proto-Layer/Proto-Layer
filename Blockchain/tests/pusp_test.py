import asyncio
import json

async def tcp_client(host="127.0.0.1", port=9000):
    reader, writer = await asyncio.open_connection(host, port)
    print(f"[+] Connected to {host}:{port}")

    request = {"command": "ping"}
    writer.write((json.dumps(request) + "\n").encode())
    await writer.drain()

    response_line = await reader.readline()
    if response_line:
        response = json.loads(response_line.decode())
        print(f"[<] Received: {response}")
    else:
        print("[!] No response received")

    writer.close()
    await writer.wait_closed()
    print("[*] Connection closed")

if __name__ == "__main__":
    asyncio.run(tcp_client())
