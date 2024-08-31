"""
Handlers for the Category page (list of sub-categories).

Handlers:
    - show_skins: Displays skins when a sub-category is selected.
    - back_to_category_page: Handles the callback for returning to the main category page.
"""

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.exceptions import DataRetrievalError
from bot.handlers.user.callbacks.skins_slider import start_skin_slider
from bot.states import ShopState
from bot.utils.callbacks import CategoryCallback, SubCategoryCallback

router = Router(name="category")


@router.callback_query(
    SubCategoryCallback.filter(F.action == "view"), ShopState.CategoryPage
)
async def show_skins(
    cb: types.CallbackQuery,
    state: FSMContext,
    callback_data: SubCategoryCallback,
    session: AsyncSession,
):
    """
    Displays skins when a sub-category is selected.

    Initiates the skin slider for the selected sub-category and updates
    the FSM state to SkinSlider. The slider starts from the first item in
    the sub-category.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        state (FSMContext): The current FSM state of the user.
        callback_data (SubCategoryCallback): The data from the callback, containing the selected sub-category ID.
        session (AsyncSession): The database session for querying skins.
    """
    try:
        sub_cat_id = callback_data.id

        skin_slider = await start_skin_slider(
            cb=cb, session=session, sub_cat_id=sub_cat_id, start_i=0
        )
        await state.update_data(skin_slider=skin_slider)
        await state.set_state(ShopState.SkinSlider)

    except DataRetrievalError:
        match msg := cb.message:
            case types.Message:
                await msg.answer(
                    "An error occurred while processing your request. Please try again later."
                )


@router.callback_query(
    CategoryCallback.filter(F.action == "back"), ShopState.CategoryPage
)
async def back_to_category_page(
    cb: types.CallbackQuery,
    state: FSMContext,
):
    """
    Handles the callback for returning to the main category page.

    Resets the FSM state to Catalog and deletes the current message.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        state (FSMContext): The current FSM state of the user.
    """

    await state.set_state(ShopState.Catalog)
    match cb.message:
        case types.Message:
            await cb.message.delete()
