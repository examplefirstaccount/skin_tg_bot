"""
This module contains handlers for the payment page.

Handlers and Functions:
    - generate_invoice: Generates an invoice dictionary for initiating payment.
    - send_invoice: Sends an invoice to the user for payment processing.
    - process_pre_checkout_query: Processes the pre-checkout query to confirm payment.
    - success_payment: Handles successful payment notifications.
"""

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
    """
    Generates an invoice for a payment request.

    Args:
        title (str): The title of the item being purchased.
        price (float): The price of the item in RUB.
        method (str): The payment method chosen by the user ('sber' or 'paymaster').

    Returns:
        dict: A dictionary containing the invoice details.
    """

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
    """
    Sends an invoice to the user based on the selected payment method.

    Converts the price to RUB using the current exchange rate, generates
    the invoice data, and sends it to the user via a Telegram invoice.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        bot (Bot): The bot instance used to send messages.
        title (str): The title of the item being purchased.
        price (float): The price of the item in USD.
        method (str): The payment method chosen by the user ('sber' or 'paymaster').
    """

    exchange_rate = get_ex_rate('RUB')
    price_rub = price * exchange_rate

    invoice_data = generate_invoice(title=title, price=round(price_rub, 2), method=method)
    await bot.send_invoice(chat_id=cb.from_user.id, **invoice_data)


@router.pre_checkout_query(ShopState.Payment)
async def process_pre_checkout_query(
        query: types.PreCheckoutQuery,
        bot: Bot
):
    """
    Processes the pre-checkout query to approve the payment.

    Approves the payment after receiving the pre-checkout query from Telegram.

    Args:
        query (types.PreCheckoutQuery): The pre-checkout query from the user.
        bot (Bot): The bot instance used to send messages.
    """

    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)


@router.message(F.types.ContentType.SUCCESSFUL_PAYMENT, ShopState.Payment)
async def success_payment(
        msg: types.Message,
        state: FSMContext
):
    """
    Handles the event when the user successfully completes a payment.

    Confirms the successful payment and sends a "Thank you" message, then
    resets the user's FSM state.

    Args:
        msg (types.Message): The message object containing the successful payment information.
        state (FSMContext): The current FSM state of the user.
    """

    if msg.successful_payment.invoice_payload == 'payment':
        await msg.answer('Thank you for your order. You will get instructions on your email.')
        await state.set_state(state=None)
