from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbacks import CategoryCallback
from bot.data.config import BACK_BTN


def get_categories(data) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for cat in data:
        builder.button(text=cat.name, callback_data=CategoryCallback(id=cat.id, action='view').pack())
    builder.button(text=' ', callback_data='#') if len(data) % 2 != 0 else None
    builder.button(text=BACK_BTN, callback_data='back_to_main_menu')

    return builder.adjust(2).as_markup()
