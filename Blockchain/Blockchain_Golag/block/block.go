import asyncio

async def verification_thread_aligner():
    """Periodically run tasks for verification thread alignment."""
    while True:
        print("Message from thread 6")
        await asyncio.sleep(3)


async def main():
    await verification_thread_aligner()


if __name__ == "__main__":
    asyncio.run(main())
