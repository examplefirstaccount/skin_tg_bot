"""
Handlers for the Catalog page (list of categories).

Handlers:
    - show_sub_categories: Displays sub-categories when a category is selected.
    - back_to_menu: Handles the callback for returning to the main menu from the catalog.
    - answer_empty_callback: Handles empty callback data without any action.
"""

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states import ShopState
from bot.db.models import SubCategory
from bot.utils.callbacks import CategoryCallback
from bot.keyboards.inline import get_sub_cats

router = Router(name='catalog')


@router.callback_query(CategoryCallback.filter(F.action == 'view'), ShopState.Catalog)
async def show_sub_categories(
        cb: types.CallbackQuery,
        state: FSMContext,
        callback_data: CategoryCallback,
        session: AsyncSession
):
    """
    Displays sub-categories when a category is selected.

    Fetches sub-categories from the database based on the selected category ID,
    updates the FSM state, and sends the sub-categories as an inline keyboard.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        state (FSMContext): The current FSM state of the user.
        callback_data (CategoryCallback): The data from the callback, containing the selected category ID.
        session (AsyncSession): The database session for querying sub-categories.
    """

    cat_id = callback_data.id
    sql_query = select(SubCategory).filter_by(category_id=cat_id)
    result = await session.execute(sql_query)
    data = result.scalars().all()

    await state.set_state(ShopState.CategoryPage)
    await state.update_data(cat_id=cat_id)
    await cb.message.answer('Here are all items in category', reply_markup=get_sub_cats(cat_id=cat_id, data=data))


@router.callback_query(F.data == 'back_to_main_menu', ShopState.Catalog)
async def back_to_menu(cb: types.CallbackQuery):
    """
    Handles the callback for returning to the main menu from the catalog.

    Deletes the current message without changing the FSM state.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
    """
    await cb.message.delete()


@router.callback_query(F.data == '#')
async def answer_empty_callback(cb: types.CallbackQuery):
    """
    Handles empty callback data without any action.

    Some inline buttons are made just for design purposes and does not have meaningful callback.
    This function just answers on such callbacks, nothing more.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
    """
    await cb.answer()
