from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbacks import SkinTypeCallback
from bot.data.config import BACK_BTN


def get_skin_types(typ_1: list[str, float], typ_2: list[str, float]) -> InlineKeyboardMarkup:
    """
    Creates a keyboard for choosing between types of skins Basic or StatTrack / Souvenir.

    Generates buttons for each skin type, including the price and an action button to choose the type,
    along with a back button to return to the previous menu.

    Args:
        typ_1 (list): The Basic skin type, with a name and price.
        typ_2 (list): The StatTrack / Souvenir skin type, with a name and price.

    Returns:
        InlineKeyboardMarkup: The constructed keyboard with skin type options.
    """
    builder = InlineKeyboardBuilder()

    builder.button(text=typ_1[0], callback_data=SkinTypeCallback(name=typ_1[0], price=typ_1[1], action='choose').pack())
    builder.button(text=typ_2[0], callback_data=SkinTypeCallback(name=typ_2[0], price=typ_2[1], action='choose').pack())
    builder.button(text=BACK_BTN, callback_data='back_to_ext_slider')

    return builder.adjust(2).as_markup()
