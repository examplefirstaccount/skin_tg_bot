"""
This module contains handlers for skin type selection and payment method selection pages.

Handlers:
    - send_payment_methods: Handles the selection of skin types and prompts the user to choose a payment method.
    - back_to_ext_slider: Handles the callback for going back to the exterior slider from the skin type selection page.
    - start_payment: Initiates the payment process after a payment method is selected.
    - back_from_payment_methods: Handles the callback for going back from the payment methods page.
"""

from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext

from bot.handlers.user.payment import send_invoice
from bot.keyboards.inline import get_payment_methods
from bot.states import ShopState
from bot.utils.callbacks import PaymentCallback, SkinTypeCallback

router = Router(name="pre_invoice")


@router.callback_query(
    SkinTypeCallback.filter(F.action == "choose"), ShopState.ChooseSkinType
)
async def send_payment_methods(
    cb: types.CallbackQuery, state: FSMContext, callback_data: SkinTypeCallback
):
    """
    Handles the callback when a user chooses a skin type.

    Updates the FSM state with the selected skin type and price,
    then prompts the user to select a payment method.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        state (FSMContext): The current FSM state of the user.
        callback_data (SkinTypeCallback): The data from the callback, containing the chosen skin type and price.
    """

    buy_type = callback_data.name
    buy_price = callback_data.price

    await state.update_data(
        buy_type=buy_type, buy_price=buy_price, skipped_skin_type_choosing=False
    )
    await state.set_state(ShopState.ChoosePaymentMethod)
    match msg := cb.message:
        case types.Message:
            await msg.answer(
                "Choose payment method", reply_markup=get_payment_methods()
            )
        case _:
            print("Message to be answered is inaccessible or missing")


@router.callback_query(F.data == "back_to_ext_slider", ShopState.ChooseSkinType)
async def back_to_ext_slider(cb: types.CallbackQuery, state: FSMContext):
    """
    Handles the callback to return to the exterior slider from the skin type choosing page.

    Changes the state back to the exterior slider and deletes the current message.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        state (FSMContext): The current FSM state of the user.
    """

    await state.set_state(ShopState.ExtSlider)
    match cb.message:
        case types.Message:
            await cb.message.delete()
        case _:
            print("Message to be deleted is inaccessible or missing")


@router.callback_query(
    PaymentCallback.filter(F.action == "choose"), ShopState.ChoosePaymentMethod
)
async def start_payment(
    cb: types.CallbackQuery, bot: Bot, state: FSMContext, callback_data: PaymentCallback
):
    """
    Initiates the payment process once the user selects a payment method.

    Retrieves the necessary data from the state, constructs the payment title, and calls
    the `send_invoice` function to send the payment invoice to the user.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        bot (Bot): The bot instance used to send messages.
        state (FSMContext): The current FSM state of the user.
        callback_data (PaymentCallback): The data from the callback, containing the chosen payment method.
    """

    method = callback_data.method
    state_data = await state.get_data()

    buy_title = state_data["buy_title"]
    buy_type = state_data["buy_type"]
    buy_price = state_data["buy_price"]

    title = f"{buy_type} {buy_title}" if buy_type != "Basic" else buy_title

    await state.set_state(ShopState.Payment)
    await send_invoice(cb=cb, bot=bot, title=title, price=buy_price, method=method)


@router.callback_query(F.data == "back_from_pay_methods", ShopState.ChoosePaymentMethod)
async def back_from_payment_methods(cb: types.CallbackQuery, state: FSMContext):
    """
    Handles the callback to go back from the payment methods page.

    Checks if the skin type selection was skipped; if so, sets the state back to the exterior slider,
    otherwise sets it back to the skin type selection. Deletes the current message.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        state (FSMContext): The current FSM state of the user.
    """

    state_data = await state.get_data()
    skipped = state_data["skipped_skin_type_choosing"]

    if skipped:
        await state.set_state(ShopState.ExtSlider)
    else:
        await state.set_state(ShopState.ChooseSkinType)

    match cb.message:
        case types.Message:
            await cb.message.delete()
        case _:
            print("Message to be deleted is inaccessible or missing")
