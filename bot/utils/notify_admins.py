import logging

from aiogram import Bot

from bot.data import config


async def on_startup_notify(bot: Bot):
    """
    Sends a startup notification to admins when the bot is launched.

    Args:
        bot (Bot): The instance of the bot used to send the notification.

    Raises:
        Exception: If the notification could not be sent due to communication issues.
    """
    for admin in config.ADMINS:
        try:
            text = 'Bot started'
            await bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logging.exception(err)
