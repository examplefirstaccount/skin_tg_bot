from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbacks import SkinCallback, ExtCallback


def get_skin_slider_menu(skin_id: int, curr_pos: int, skins_count: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='❮', callback_data='prev_skin')
    builder.button(text=f'{curr_pos}/{skins_count}', callback_data='#')
    builder.button(text='❯', callback_data='next_skin')
    builder.button(text='Buy', callback_data=SkinCallback(id=skin_id, action='view').pack())
    builder.button(text='Back', callback_data='back_to_sub_cat_page')

    return builder.adjust(3).as_markup()


def get_ext_slider_menu(skin_ext: str, curr_pos: int, skins_count: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='❮', callback_data='prev_ext')
    builder.button(text=f'{curr_pos}/{skins_count}', callback_data='#')
    builder.button(text='❯', callback_data='next_ext')
    builder.button(text='Buy', callback_data=ExtCallback(name=skin_ext, action='buy').pack())
    builder.button(text='Back', callback_data='back_to_skin_slider')

    return builder.adjust(3).as_markup()
