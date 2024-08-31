from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_default_commands(bot: Bot):
    """
    Sets the default commands for the bot that are visible to users in private chats.

    Args:
        bot (Bot): The instance of the bot where commands are to be set.

    Commands set:
        - /start: Start bot
        - /help: Contact with moderators
        - /shop: Open shop catalog

    Raises:
        Exception: If the commands could not be set due to API errors.
    """
    commands = [
        BotCommand(command="start", description="Start bot"),
        BotCommand(command="help", description="Contact with moderators"),
        BotCommand(command="shop", description="Open shop catalog"),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
