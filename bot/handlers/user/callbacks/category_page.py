"""The file contains handlers for Category page (list of sub categories)"""


from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from bot.states import ShopState
from bot.handlers.user.callbacks.skins_slider import start_skin_slider
from bot.utils.callbacks import CategoryCallback, SubCategoryCallback

router = Router(name='category')


@router.callback_query(SubCategoryCallback.filter(F.action == 'view'), ShopState.CategoryPage)
async def show_skins(
        cb: types.CallbackQuery,
        state: FSMContext,
        callback_data: SubCategoryCallback,
        session: AsyncSession
):

    sub_cat_id = callback_data.id

    skin_slider = await start_skin_slider(cb=cb, session=session, sub_cat_id=sub_cat_id, start_i=0)
    await state.update_data(skin_slider=skin_slider)
    await state.set_state(ShopState.SkinSlider)


@router.callback_query(CategoryCallback.filter(F.action == 'back'), ShopState.CategoryPage)
async def back_to_category_page(
        cb: types.CallbackQuery,
        state: FSMContext,
):

    await state.set_state(ShopState.Catalog)
    await cb.message.delete()
