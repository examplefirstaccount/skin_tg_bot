from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Start bot'),
        BotCommand(command='help', description='Contact with moderators'),
        BotCommand(command='shop', description='Open shop catalog')
    ]

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats()
    )
