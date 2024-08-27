from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbacks import PaymentCallback


def get_payment_methods() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Sber', callback_data=PaymentCallback(method='sber', action='choose').pack())
    builder.button(text='Paymaster', callback_data=PaymentCallback(method='paymaster', action='choose').pack())
    builder.button(text='Back', callback_data='back_from_pay_methods')

    return builder.adjust(2).as_markup()
