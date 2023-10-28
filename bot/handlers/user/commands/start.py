"""Handler for /start command"""


from aiogram import types, Router
from aiogram.filters import CommandStart


def get_start_msg(name: str):
    return f"""Hello {name} 👋
🤖 Welcome to the skin shop bot.

🛍️ Use /shop command to go to the catalog.
💰 Payment methods: PayMaster, Sber and Qiwi.

❓ Something went wrong? Type /help and admins solve ur problem"""


router = Router(name='start')


@router.message(CommandStart())
async def command_start(msg: types.Message):

    await msg.answer(text=get_start_msg(msg.from_user.full_name))
