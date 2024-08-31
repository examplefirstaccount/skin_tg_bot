from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data.config import BACK_BTN, PAYMASTER_ICON, SBER_ICON
from bot.utils.callbacks import PaymentCallback


def get_payment_methods() -> InlineKeyboardMarkup:
    """
    Creates a keyboard for selecting a payment method.

    Generates buttons for available payment methods, including Sber and PayMaster,
    along with a back button to return to the previous menu.

    Returns:
        InlineKeyboardMarkup: The constructed keyboard with payment method options.
    """
    builder = InlineKeyboardBuilder()

    builder.button(
        text=SBER_ICON,
        callback_data=PaymentCallback(method="sber", action="choose").pack(),
    )
    builder.button(
        text=PAYMASTER_ICON,
        callback_data=PaymentCallback(method="paymaster", action="choose").pack(),
    )
    builder.button(text=BACK_BTN, callback_data="back_from_pay_methods")
    builder.adjust(2)

    return builder.as_markup()
