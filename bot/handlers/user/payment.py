"""The file contains handlers for Payment page"""


from aiogram import types, Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice

from bot.data.config import TOKEN_SBER, TOKEN_PAYMASTER
from bot.states import ShopState
from bot.utils.api.skins import get_ex_rate

router = Router(name='payment')


def generate_invoice(
        title: str,
        price: float,
        method: str
) -> dict:

    tokens = {'sber': TOKEN_SBER, 'paymaster': TOKEN_PAYMASTER}
    return {'title': title,
            'description': 'good choice',
            'payload': 'payment',
            'provider_token': tokens[method],
            'currency': 'RUB',
            'start_parameter': 'testing_bot',
            'prices': [LabeledPrice(label=title, amount=int(price*100))],
            'need_email': True
            }


async def send_invoice(
        cb: types.CallbackQuery,
        bot: Bot,
        title: str,
        price: float,
        method: str
):

    exchange_rate = get_ex_rate('RUB')
    price_rub = price * exchange_rate

    invoice_data = generate_invoice(title=title, price=round(price_rub, 2), method=method)
    await bot.send_invoice(chat_id=cb.from_user.id, **invoice_data)


@router.pre_checkout_query(ShopState.Payment)
async def process_pre_checkout_query(
        query: types.PreCheckoutQuery,
        bot: Bot
):

    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)


@router.message(F.types.ContentType.SUCCESSFUL_PAYMENT, ShopState.Payment)
async def success_payment(
        msg: types.Message,
        state: FSMContext
):

    if msg.successful_payment.invoice_payload == 'payment':
        await msg.answer('Thank you for your order. You will get instructions on your email.')
        await state.set_state(state=None)
