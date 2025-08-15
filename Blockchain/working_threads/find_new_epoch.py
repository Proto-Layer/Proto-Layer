import asyncio

async def find_new_epoch():
    """Simulate a thread that looks for new epochs periodically."""
    while True:
        print("Message from thread 3")
        await asyncio.sleep(3)


async def main():
    await find_new_epoch()


if __name__ == "__main__":
    asyncio.run(main())
