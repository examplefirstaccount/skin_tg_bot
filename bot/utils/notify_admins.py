import logging

from aiogram import Bot

from bot.data import config


async def on_startup_notify(bot: Bot):
    for admin in config.ADMINS:
        try:
            text = 'Bot started'
            await bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logging.exception(err)
