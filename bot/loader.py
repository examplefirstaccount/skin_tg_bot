from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.base import BaseStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.middlewares import DbSessionMiddleware
from bot.handlers.user import user_routers


def get_dispatcher(session_pool: async_sessionmaker, storage: BaseStorage = MemoryStorage()):
    dp = Dispatcher(storage=storage)

    dp.update.middleware(DbSessionMiddleware(session_pool=session_pool))
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    for router in user_routers:
        dp.include_router(router)

    return dp
