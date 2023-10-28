import asyncio
import logging

from aiogram import Bot
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
    bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')

    # redis = Redis()
    # storage = RedisStorage(redis=redis)

    # dp = get_dispatcher(storage=storage, session_pool=sessionmaker)

    dp = get_dispatcher(session_pool=sessionmaker)

    await set_default_commands(bot=bot)
    await on_startup_notify(bot=bot)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

# TODO: try to add shop cart after all steps above
# TODO: try to add user profile, settings etc.
# TODO: start slider on category page if there are too much weapons

# -- Aiogram
# https://www.youtube.com/playlist?list=PLN0sMOjX-lm5BMwTm-llmJuA50umZJOsL - video guide for aiogram 3.0
# https://mastergroosha.github.io/aiogram-3-guide/ - text guide for aiogram 3.0
# https://github.com/MasterGroosha/aiogram-and-sqlalchemy-demo/tree/master/bot/
# https://github.com/MassonNN/masson-aiogram-template

# https://docs.pyrogram.org/intro/quickstart - after aiogram 2.0 and 3.0 move to pyrogram


# -- GitHub
# https://github.com/TimNekk?tab=overview&from=2023-07-01&to=2023-07-16 - good github profile


# -- Redis
# https://blog.logrocket.com/guide-to-fully-understanding-redis/
# https://www.tutorialspoint.com/redis/redis_quick_guide.htm


# -- SQLAlchemy
# https://www.youtube.com/watch?v=hkvngd_BUrY - async


# -- SQL template for online shop
# https://mysql.tutorials24x7.com/blog/guide-to-design-database-for-shopping-cart-in-mysql


# -- Perfect images for skin bot, but hard to parse (no exteriors, just Factory new)
# https://cdn.csgoskins.gg/public/videos/floats/v1/embedding/galil-ar-orange-ddpat.webm


# -- Asyncio
# https://docs.python.org/3/library/asyncio-task.html


# catalog page = list of categories e.g. Knives, Rifles etc.
# category page = list of sub_categories e.g. AK-47, M4A1-S, etc. for Rifles category
# sub_category page | skin slider page = list of products e.g. for AK-47: Ice-Coaled, Asimov etc.
# product page | ext slider page  = image, price and ext (Factory New, Minimal Wear, Field-Tested, etc.)
