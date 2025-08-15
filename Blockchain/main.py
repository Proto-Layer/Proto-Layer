import asyncio

from tcp_server.server import start_tcp_server
from working_threads.block_generation import block_generation
from working_threads.block_sharing_and_proofs_grabbing import block_sharing
from working_threads.find_new_epoch import find_new_epoch
from working_threads.leader_rotation import leader_rotation
from working_threads.next_epoch_proposer import next_epoch_proposer
from working_threads.verification_thread_aligner import verification_thread_aligner


async def run_node():
    """Launch ProtoLayer node services and worker routines."""
    tcp_task = asyncio.create_task(start_tcp_server())

    workers = [
        asyncio.create_task(block_generation()),
        asyncio.create_task(block_sharing()),
        asyncio.create_task(find_new_epoch()),
        asyncio.create_task(leader_rotation()),
        asyncio.create_task(next_epoch_proposer()),
        asyncio.create_task(verification_thread_aligner())
    ]

    try:
        await tcp_task
    except asyncio.CancelledError:
        print("[!] Node services shutting down...")
    finally:
        for task in [tcp_task, *workers]:
            task.cancel()
        await asyncio.gather(tcp_task, *workers, return_exceptions=True)


def terminate(loop: asyncio.AbstractEventLoop) -> None:
    """Cancel all running tasks in the loop."""
    for task in asyncio.all_tasks(loop):
        task.cancel()


if __name__ == "__main__":
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    try:
        event_loop.run_until_complete(run_node())
    except KeyboardInterrupt:
        print("\n[*] Graceful shutdown initiated...")
        terminate(event_loop)
        event_loop.run_until_complete(asyncio.sleep(0.1))
    finally:
        event_loop.close()
