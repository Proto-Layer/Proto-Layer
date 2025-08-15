import asyncio

async def block_generation():
    """Simulate a block generation thread that prints a message periodically."""
    while True:
        print("Message from thread 1")
        await asyncio.sleep(3)


async def main():
    await block_generation()


if __name__ == "__main__":
    asyncio.run(main())
