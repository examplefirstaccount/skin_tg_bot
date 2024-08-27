"""The file contains handlers for Catalog page (list of categories)"""


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

    cat_id = callback_data.id
    sql_query = select(SubCategory).filter_by(category_id=cat_id)
    result = await session.execute(sql_query)
    data = result.scalars().all()

    await state.set_state(ShopState.CategoryPage)
    await state.update_data(cat_id=cat_id)
    await cb.message.answer('Here are all items in category', reply_markup=get_sub_cats(cat_id=cat_id, data=data))


@router.callback_query(F.data == 'back_to_main_menu', ShopState.Catalog)
async def back_to_menu(cb: types.CallbackQuery):

    await cb.message.delete()


@router.callback_query(F.data == '#')
async def answer_empty_callback(cb: types.CallbackQuery):

    await cb.answer()
