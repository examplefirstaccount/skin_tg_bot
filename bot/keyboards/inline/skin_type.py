from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbacks import SkinTypeCallback


def get_skin_types(typ_1: list[str, float], typ_2: list[str, float]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=typ_1[0], callback_data=SkinTypeCallback(name=typ_1[0], price=typ_1[1], action='choose').pack())
    builder.button(text=typ_2[0], callback_data=SkinTypeCallback(name=typ_2[0], price=typ_2[1], action='choose').pack())
    builder.button(text='Back', callback_data='back_to_ext_slider')

    return builder.adjust(2).as_markup()
