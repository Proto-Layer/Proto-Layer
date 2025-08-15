import asyncio

async def next_epoch_proposer():
    """Periodically run tasks related to proposing the next epoch."""
    while True:
        print("Message from thread 5")
        await asyncio.sleep(3)


async def main():
    await next_epoch_proposer()


if __name__ == "__main__":
    asyncio.run(main())
