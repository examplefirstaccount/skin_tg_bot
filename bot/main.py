import asyncio
import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.data import config
from bot.loader import get_dispatcher
from bot.utils.notify_admins import on_startup_notify
from bot.utils.set_bot_commands import set_default_commands


async def main():
    """
    Main entry point for the bot's asynchronous execution.
    Sets up the database engine, session maker, bot instance, Redis storage,
    and dispatcher, then starts the bot's polling process.

    Steps:
    1. Creates the async database engine and session maker.
    2. Initializes the bot with default settings and Redis storage.
    3. Sets default bot commands.
    4. Notifies admins about the bot startup.
    5. Starts the dispatcher for polling.

    Raises:
        Exception: If any initialization fails or during bot startup.
    """
    engine = create_async_engine(url=config.POSTGRES_URI)
    sessionmaker = async_sessionmaker(bind=engine)
    default = DefaultBotProperties(parse_mode='HTML')
    bot = Bot(token=config.BOT_TOKEN, default=default)

    redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)
    storage = RedisStorage(redis=redis)

    dp = get_dispatcher(storage=storage, session_pool=sessionmaker)

    await set_default_commands(bot=bot)
    await on_startup_notify(bot=bot)

    await dp.start_polling(bot)


def run():
    """
    Configures logging and runs the main bot function in an asynchronous event loop.

    This function sets the logging level to INFO and initializes the event loop
    to run the bot's main asynchronous operations.

    Raises:
        RuntimeError: If the event loop fails to start.
    """
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())


if __name__ == '__main__':
    run()
