"""
Handler for the /shop command.

Handler:
    - show_categories: Displays available categories when the user enters the /shop command.
"""

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Category
from bot.keyboards.inline import get_categories
from bot.states import ShopState

router = Router(name="shop")


@router.message(Command(commands="shop"))
async def show_categories(msg: types.Message, state: FSMContext, session: AsyncSession):
    """
    Displays a list of all categories available in the shop.

    Fetches categories from the database, updates the FSM state to Catalog,
    and sends the categories as an inline keyboard to the user.

    Args:
        msg (types.Message): The message object containing the /shop command from the user.
        state (FSMContext): The current FSM state of the user.
        session (AsyncSession): The database session for querying categories.
    """

    sql_query = select(Category)
    result = await session.execute(sql_query)
    data = result.scalars().all()
    if len(data) == 0:
        await msg.answer(
            "An error occurred while processing your request. Please try again later."
        )

    await state.set_state(ShopState.Catalog)
    await msg.answer("Here are all categories", reply_markup=get_categories(data=data))
