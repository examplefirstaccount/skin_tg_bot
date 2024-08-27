from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbacks import SubCategoryCallback, CategoryCallback


def get_sub_cats(cat_id: int, data) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for sub in data:
        builder.button(text=sub.name, callback_data=SubCategoryCallback(id=sub.id, action='view').pack())
    builder.button(text=' ', callback_data='#') if len(data) % 2 != 0 else None
    builder.button(text='Back', callback_data=CategoryCallback(id=cat_id, action='back').pack())

    return builder.adjust(2).as_markup()
