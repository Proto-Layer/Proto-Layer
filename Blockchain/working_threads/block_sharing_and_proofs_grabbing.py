import asyncio

async def block_sharing():
    """Simulate a block sharing thread that prints a message periodically."""
    while True:
        print("Message from thread 2")
        await asyncio.sleep(3)


async def main():
    await block_sharing()


if __name__ == "__main__":
    asyncio.run(main())
