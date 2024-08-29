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
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())


if __name__ == '__main__':
    run()
