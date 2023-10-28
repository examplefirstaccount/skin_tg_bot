"""Handler for /help command"""


from aiogram import types, Router
from aiogram.filters import Command

router = Router(name='help')


@router.message(Command(commands='help'))
async def command_help(msg: types.Message):

    await msg.answer(f'Hey {msg.from_user.first_name}, you need help?')
