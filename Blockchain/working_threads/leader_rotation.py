import asyncio

from structures.threads_metadata_handlers import ApprovementThreadMetadataHandler
from utils import get_utc_timestamp
from global_vars import APPROVEMENT_THREAD


def time_is_out_for_current_leader(thread: ApprovementThreadMetadataHandler) -> bool:
    """Check if the leadership time for the current leader has expired."""
    leadership_timeframe = thread.network_parameters.get("LEADERSHIP_TIMEFRAME")
    current_leader_index = thread.epoch.current_leader_index

    return get_utc_timestamp() >= thread.epoch.start_timestamp + (current_leader_index + 1) * leadership_timeframe


async def leader_rotation():
    """Periodically check for leader rotation."""
    while True:
        # TODO: Set mutex here
        epochHandlerRef = APPROVEMENT_THREAD.epoch
        have_next_candidate = epochHandlerRef.current_leader_index + 1 < len(epochHandlerRef.leaders_sequence)

        if have_next_candidate and time_is_out_for_current_leader(APPROVEMENT_THREAD):
            # TODO: rotate leader
            pass

        await asyncio.sleep(3)


async def main():
    await leader_rotation()


if __name__ == "__main__":
    asyncio.run(main())
