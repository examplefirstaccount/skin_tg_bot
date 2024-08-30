from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbacks import SubCategoryCallback, CategoryCallback
from bot.data.config import BACK_BTN


def get_sub_cats(cat_id: int, data) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard for subcategories within a category.

    Generates buttons for each subcategory, with an additional back button to return
    to the previous category page.

    Args:
        cat_id (int): The ID of the current category.
        data (list): A list of subcategory objects, each with a name and ID.

    Returns:
        InlineKeyboardMarkup: The constructed keyboard with subcategory buttons.
    """
    builder = InlineKeyboardBuilder()

    for sub in data:
        builder.button(text=sub.name, callback_data=SubCategoryCallback(id=sub.id, action='view').pack())
    builder.button(text=' ', callback_data='#') if len(data) % 2 != 0 else None
    builder.button(text=BACK_BTN, callback_data=CategoryCallback(id=cat_id, action='back').pack())

    return builder.adjust(2).as_markup()
