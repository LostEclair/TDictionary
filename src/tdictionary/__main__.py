from .bot import run_bot
from asyncio import run
from .database import initialize_database


async def prepare() -> None:
    """
    прелюдии какието
    """
    await initialize_database()


run(prepare())
run(run_bot())
