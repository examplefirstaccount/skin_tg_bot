"""
Handler for the /help command.

Handler:
    - command_help: Sends a help message to the user when they use the /help command.
"""

from aiogram import Router, types
from aiogram.filters import Command

router = Router(name="help")


@router.message(Command(commands="help"))
async def command_help(msg: types.Message):
    """
    Sends a help message to the user.

    Args:
        msg (types.Message): The message object containing the /help command from the user.
    """
    match user := msg.from_user:
        case types.User():
            await msg.answer(f"Hey {user.first_name}, you need help?")
        case None:
            await msg.answer("Hey, you need help?")
