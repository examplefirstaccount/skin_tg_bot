from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker


class DbSessionMiddleware(BaseMiddleware):
    """
    Middleware to provide a database session for each update.

    This middleware injects a database session into the handler's data, allowing the handler
    to perform database operations. The session is automatically closed after the handler is executed.

    Attributes:
        session_pool (async_sessionmaker): The session maker for creating new database sessions.
    """

    def __init__(self, session_pool: async_sessionmaker):
        """
        Initializes the middleware with a session maker.

        Args:
            session_pool (async_sessionmaker): The session pool for creating new database sessions.
        """
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Middleware call method to provide a session to the handler.

        Args:
            handler (Callable): The handler function to be called.
            event (TelegramObject): The Telegram event that triggered the handler.
            data (Dict[str, Any]): The data dictionary passed to the handler.

        Returns:
            Any: The result of the handler execution.
        """
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)
