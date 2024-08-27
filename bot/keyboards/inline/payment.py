from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbacks import PaymentCallback
from bot.data.config import BACK_BTN, SBER_ICON, PAYMASTER_ICON


def get_payment_methods() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=SBER_ICON, callback_data=PaymentCallback(method='sber', action='choose').pack())
    builder.button(text=PAYMASTER_ICON, callback_data=PaymentCallback(method='paymaster', action='choose').pack())
    builder.button(text=BACK_BTN, callback_data='back_from_pay_methods')

    return builder.adjust(2).as_markup()
