from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data.config import BACK_BTN, BUY_BTN, LEFT_BTN, RIGHT_BTN
from bot.utils.callbacks import ExtCallback, SkinCallback


def get_skin_slider_menu(
    skin_id: int, curr_pos: int, skins_count: int
) -> InlineKeyboardMarkup:
    """
    Creates a slider navigation keyboard for browsing skins.

    The slider includes navigation buttons to move left or right, a button to view the
    current position, a buy button, and a back button.

    Args:
        skin_id (int): The ID of the current skin.
        curr_pos (int): The current position in the slider.
        skins_count (int): The total number of skins available.

    Returns:
        InlineKeyboardMarkup: The constructed keyboard for skin slider navigation.
    """
    builder = InlineKeyboardBuilder()

    builder.button(text=LEFT_BTN, callback_data="prev_skin")
    builder.button(text=f"{curr_pos}/{skins_count}", callback_data="#")
    builder.button(text=RIGHT_BTN, callback_data="next_skin")
    builder.button(
        text=BUY_BTN, callback_data=SkinCallback(id=skin_id, action="view").pack()
    )
    builder.button(text=BACK_BTN, callback_data="back_to_sub_cat_page")
    builder.adjust(3)

    return builder.as_markup()


def get_ext_slider_menu(
    skin_ext: str, curr_pos: int, skins_count: int
) -> InlineKeyboardMarkup:
    """
    Creates a slider navigation keyboard for browsing skin exteriors.

    The slider includes navigation buttons to move left or right, a button to view the
    current position, a buy button, and a back button.

    Args:
        skin_ext (str): The exterior of the current skin.
        curr_pos (int): The current position in the slider.
        skins_count (int): The total number of skin exteriors available.

    Returns:
        InlineKeyboardMarkup: The constructed keyboard for exterior slider navigation.
    """
    builder = InlineKeyboardBuilder()

    builder.button(text=LEFT_BTN, callback_data="prev_ext")
    builder.button(text=f"{curr_pos}/{skins_count}", callback_data="#")
    builder.button(text=RIGHT_BTN, callback_data="next_ext")
    builder.button(
        text=BUY_BTN, callback_data=ExtCallback(name=skin_ext, action="buy").pack()
    )
    builder.button(text=BACK_BTN, callback_data="back_to_skin_slider")
    builder.adjust(3)

    return builder.as_markup()
