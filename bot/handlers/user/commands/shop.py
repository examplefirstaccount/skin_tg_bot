"""Handler for /shop command"""

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states import ShopState
from bot.db.models import Category
from bot.keyboards.inline import get_categories

router = Router(name='shop')


@router.message(Command(commands='shop'))
async def show_categories(
        msg: types.Message,
        state: FSMContext,
        session: AsyncSession
):

    sql_query = select(Category)
    result = await session.execute(sql_query)
    data = result.scalars().all()

    await state.set_state(ShopState.Catalog)
    await msg.answer('Here are all categories', reply_markup=get_categories(data=data))
