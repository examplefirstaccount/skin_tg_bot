"""The file contains handlers for Skin type and Payment method choosing pages"""


from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext

from bot.states import ShopState
from bot.handlers.user.payment import send_invoice
from bot.utils.callbacks import PaymentCallback, SkinTypeCallback
from bot.keyboards.inline import get_payment_methods

router = Router(name='pre_invoice')


@router.callback_query(SkinTypeCallback.filter(F.action == 'choose'), ShopState.ChooseSkinType)
async def send_payment_methods(
        cb: types.CallbackQuery,
        state: FSMContext,
        callback_data: SkinTypeCallback
):

    buy_type = callback_data.name
    buy_price = callback_data.price

    await state.update_data(buy_type=buy_type, buy_price=buy_price, skipped_skin_type_choosing=False)
    await state.set_state(ShopState.ChoosePaymentMethod)
    await cb.message.answer('Choose payment method', reply_markup=get_payment_methods())


@router.callback_query(F.data == 'back_to_ext_slider', ShopState.ChooseSkinType)
async def back_to_ext_slider(
        cb: types.CallbackQuery,
        state: FSMContext
):

    await state.set_state(ShopState.ExtSlider)
    await cb.message.delete()


@router.callback_query(PaymentCallback.filter(F.action == 'choose'), ShopState.ChoosePaymentMethod)
async def start_payment(
        cb: types.CallbackQuery,
        bot: Bot,
        state: FSMContext,
        callback_data: PaymentCallback
):

    method = callback_data.method
    state_data = await state.get_data()

    buy_title = state_data['buy_title']
    buy_type = state_data['buy_type']
    buy_price = state_data['buy_price']

    title = f'{buy_type} {buy_title}' if buy_type != 'Basic' else buy_title

    await state.set_state(ShopState.Payment)
    await send_invoice(cb=cb, bot=bot, title=title, price=buy_price, method=method)


@router.callback_query(F.data == 'back_from_pay_methods', ShopState.ChoosePaymentMethod)
async def back_from_payment_methods(
        cb: types.CallbackQuery,
        state: FSMContext
):

    state_data = await state.get_data()
    skipped = state_data['skipped_skin_type_choosing']

    if skipped:
        await state.set_state(ShopState.ExtSlider)
    else:
        await state.set_state(ShopState.ChooseSkinType)

    await cb.message.delete()
