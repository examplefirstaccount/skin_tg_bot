from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data.config import BACK_BTN
from bot.utils.callbacks import CategoryCallback


def get_categories(data) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard for browsing categories.

    Generates buttons for each category and includes a back button to return to the main menu.

    Args:
        data: A list of category objects, each with a name and ID.

    Returns:
        InlineKeyboardMarkup: The constructed keyboard with category buttons.
    """
    builder = InlineKeyboardBuilder()

    for cat in data:
        builder.button(
            text=cat.name,
            callback_data=CategoryCallback(id=cat.id, action="view").pack(),
        )
    builder.button(text=" ", callback_data="#") if len(data) % 2 != 0 else None
    builder.button(text=BACK_BTN, callback_data="back_to_main_menu")
    builder.adjust(2)

    return builder.as_markup()
