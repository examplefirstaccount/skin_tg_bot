"""
Handler for the /start command.

Handlers:
    - command_start: Sends a welcome message to the user when they use the /start command.
"""

from aiogram import Router, types
from aiogram.filters import CommandStart


def get_start_msg(name: str = ""):
    """
    Generates a welcome message for the user.

    Args:
        name (str): The name of the user.

    Returns:
        str: A formatted welcome message.
    """

    return f"""Hello {name} 👋
🤖 Welcome to the skin shop bot.

🛍️ Use /shop command to go to the catalog.
💰 Payment methods: PayMaster and Sber.

❓ Something went wrong? Type /help and admins solve ur problem"""


router = Router(name="start")


@router.message(CommandStart())
async def command_start(msg: types.Message):
    """
    Sends a welcome message to the user when they use the /start command.

    Args:
        msg (types.Message): The message object containing the /start command from the user.
    """
    match user := msg.from_user:
        case types.User():
            await msg.answer(text=get_start_msg(user.full_name))
        case None:
            await msg.answer(text=get_start_msg())
