"""
Handlers for the Ext slider (list of exteriors for skins).

Handlers:
    - update_slider: Handles navigation through the exterior slider (next/previous).
    - buy_skin: Handles the process of initiating a skin purchase.
    - back_to_skin_slider: Handles the callback to return to the skin slider.
Utilities:
    - get_ext_caption: Generates a formatted caption for the exterior slider.
    - get_ext_data: Retrieves data for the exterior slider, including images and prices.
    - start_ext_slider: Initializes the exterior slider with the first exterior in the list.
"""

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.utils import markdown as fmt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.data.config import LG_EXTERIORS
from bot.db.models import Exterior as Ext
from bot.db.models import Skin
from bot.exceptions import DataRetrievalError
from bot.keyboards.inline import (
    get_ext_slider_menu,
    get_payment_methods,
    get_skin_types,
)
from bot.states import ShopState
from bot.utils.api.skins import get_ext_images, get_ext_prices
from bot.utils.callbacks import ExtCallback

router = Router(name="exterior_slider")


def get_ext_caption(
    skin_name: str, skin_type: str, ext: str, price: float, spec_price: float
) -> str:
    """
    Generates a formatted caption for the exterior slider.

    Formats the caption based on skin name, type, exterior, and prices. Displays basic
    and special prices if applicable.

    Args:
        skin_name (str): The name of the skin.
        skin_type (str): The type of the skin (e.g., 'Normal', 'StatTrak').
        ext (str): The exterior type (e.g., 'Factory New').
        price (float): The basic price of the skin.
        spec_price (float): The special price of the skin if applicable.

    Returns:
        str: A formatted string for the caption.
    """

    name = f"{skin_name} ({ext})" if ext != "none" else skin_name
    if skin_type == "Normal":
        price_line = fmt.text(fmt.hbold("Price: "), fmt.hitalic("$", price))
    else:
        # 4 spaces for italic or code, 7 space for bold
        price_line = fmt.text(
            fmt.hbold("Basic:       "),
            fmt.hitalic("$", price),
            "\n",
            "\n",
            fmt.hbold(f"{skin_type}: "),
            fmt.hitalic("$", spec_price),
            sep="",
        )
    return fmt.text(fmt.hcode(name), "\n", "\n", price_line, "\n", "\n", sep="")


async def get_ext_data(
    session: AsyncSession, skin_id: int
) -> tuple[list[dict], str, str]:
    """
    Retrieves data for the exterior slider, including images and prices.

    Queries the database for the skin's name, type, and exteriors. Fetches images and prices
    for each exterior.

    Args:
        session (AsyncSession): The database session for executing queries.
        skin_id (int): The ID of the skin to fetch data for.

    Returns:
        tuple: A tuple containing a list of exterior data, the skin type, and the skin name.
        Returns None if skin with provided skin_id was not found in database.

    Raises:
        DataRetrievalError: If no skin or no exterior was found by provided skin_id.
    """

    # Get skin's Name, Type, and Category_id by skin_id. Return None if skin is not in db.
    sql_query_skin = select(Skin.name, Skin.type, Skin.category_id).filter_by(
        id=skin_id
    )
    result_sql = await session.execute(sql_query_skin)
    row = result_sql.first()
    if row:
        skin_name, skin_type, cat_id = row
    else:
        raise DataRetrievalError(f"Data for skin_id {skin_id} was not in the database.")

    # Get all exteriors (name, basic and special prices api id) for skin with provided skin_id.
    sql_query_ext = select(Ext.ext, Ext.price_id, Ext.spec_price_id).filter_by(
        skin_id=skin_id
    )
    result_sql = await session.execute(sql_query_ext)
    ext_data = result_sql.all()
    if len(ext_data) == 0:
        raise DataRetrievalError(f"No exteriors found for skin_id {skin_id}.")

    # If skin is for Knife or Gloves (cat_id 1 or 2), then add '★' to the name (cs money API uses it fsr).
    if cat_id in [1, 2]:
        skin_name = "★ " + skin_name
    skin_ext, skin_price_ids, skin_spec_price_ids = zip(*ext_data)
    images = get_ext_images(skin_name)
    prices = get_ext_prices(list(skin_price_ids + skin_spec_price_ids))

    result: list[dict] = []
    for i in range(len(skin_ext)):
        ext = LG_EXTERIORS.get(skin_ext[i], "none")
        price_id = skin_price_ids[i]
        spec_price_id = skin_spec_price_ids[i]

        # Get prices for basic type and for special (Souvenir, StatTrack) type of the skin.
        price = prices.get(price_id, "-")
        spec_price = prices.get(spec_price_id, "-") if skin_type != "Normal" else "-"

        if ext == "none":
            img = list(images.values())[0]
            result.append(
                {"ext_name": ext, "img": img, "price": price, "spec_price": spec_price}
            )
            return result, skin_type, skin_name.replace("★ ", "")
        else:
            img = images.get(ext)

        result.append(
            {"ext_name": ext, "img": img, "price": price, "spec_price": spec_price}
        )

    return result, skin_type, skin_name.replace("★ ", "")


async def start_ext_slider(
    cb: types.CallbackQuery, session: AsyncSession, skin_id: int, start_i: int
) -> dict:
    """
    Initializes the exterior slider with the first exterior in the list.

    Fetches exterior data and displays the first exterior with its image, caption, and slider menu.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        session (AsyncSession): The database session for querying exteriors.
        skin_id (int): The ID of the skin to display exteriors for.
        start_i (int): The starting index for the slider (typically 0).

    Returns:
        dict: A dictionary containing slider data including exterior details and the current position.
    """

    ext_data, skin_type, skin_name = await get_ext_data(session, skin_id)
    slider = {
        "ext_data": ext_data,
        "skin_type": skin_type,
        "skin_name": skin_name,
        "ext_count": len(ext_data),
        "pos": start_i,
    }

    photo = ext_data[start_i]["img"]
    caption = get_ext_caption(
        skin_name=skin_name,
        skin_type=skin_type,
        ext=ext_data[start_i]["ext_name"],
        price=ext_data[start_i]["price"],
        spec_price=ext_data[start_i]["spec_price"],
    )
    reply_markup = get_ext_slider_menu(
        skin_ext=ext_data[start_i]["ext_name"],
        curr_pos=start_i + 1,
        skins_count=len(ext_data),
    )

    match msg := cb.message:
        case types.Message():
            await msg.answer_photo(
                photo=photo, caption=caption, reply_markup=reply_markup
            )
        case _:
            print("Message to be answered is inaccessible or missing")

    return slider


@router.callback_query(F.data.regexp(r"(prev|next)_ext"), ShopState.ExtSlider)
async def update_slider(cb: types.CallbackQuery, state: FSMContext):
    """
    Handles navigation through the exterior slider (next/previous).

    Updates the slider to show the next or previous exterior based on user input,
    updating the image, caption, and navigation buttons.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        state (FSMContext): The current FSM state of the user.
    """

    state_data = await state.get_data()
    slider = state_data["ext_slider"]

    ext_data = slider["ext_data"]
    past_i = slider["pos"]

    if cb.data == "prev_ext":
        curr_i = past_i - 1 if past_i != 0 else slider["ext_count"] - 1
    else:
        curr_i = past_i + 1 if past_i != slider["ext_count"] - 1 else 0

    if curr_i == past_i:
        pass
    else:
        slider["pos"] = curr_i
        caption = get_ext_caption(
            skin_name=slider["skin_name"],
            skin_type=slider["skin_type"],
            ext=ext_data[curr_i]["ext_name"],
            price=ext_data[curr_i]["price"],
            spec_price=ext_data[curr_i]["spec_price"],
        )
        reply_markup = get_ext_slider_menu(
            skin_ext=ext_data[curr_i]["ext_name"],
            curr_pos=curr_i + 1,
            skins_count=slider["ext_count"],
        )
        media = InputMediaPhoto(media=ext_data[curr_i]["img"], caption=caption)

        await state.update_data(ext_slider=slider)
        match msg := cb.message:
            case types.Message():
                await msg.edit_media(media=media)
                await msg.edit_reply_markup(reply_markup=reply_markup)
            case _:
                print("Message to be answered is inaccessible or missing")


@router.callback_query(ExtCallback.filter(F.action == "buy"), ShopState.ExtSlider)
async def buy_skin(
    cb: types.CallbackQuery,
    state: FSMContext,
):
    """
    Handles the process of initiating a skin purchase.

    Determines the type and price of the selected skin based on the current slider
    position and initiates the payment method selection.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        state (FSMContext): The current FSM state of the user.
    """

    state_data = await state.get_data()
    slider = state_data["ext_slider"]

    ext_data = slider["ext_data"]
    skin_name = slider["skin_name"]
    skin_type = slider["skin_type"]
    pos = slider["pos"]

    ext = ext_data[pos]["ext_name"]
    price = ext_data[pos]["price"]
    spec_price = ext_data[pos]["spec_price"]

    buy_title = f"{skin_name} ({ext})" if ext != "none" else skin_name

    await state.update_data(buy_title=buy_title)

    if skin_type == "Normal" or ((price == "-") ^ (spec_price == "-")):
        buy_type = "Basic" if spec_price == "-" else skin_type
        buy_price = price if spec_price == "-" else spec_price

        await state.update_data(
            buy_type=buy_type, buy_price=buy_price, skipped_skin_type_choosing=True
        )
        await state.set_state(ShopState.ChoosePaymentMethod)
        match msg := cb.message:
            case types.Message():
                await msg.answer(
                    "Choose payment method", reply_markup=get_payment_methods()
                )
            case _:
                print("Message to be answered is inaccessible or missing")
    else:
        reply_markup = get_skin_types(("Basic", price), (skin_type, spec_price))

        await state.set_state(ShopState.ChooseSkinType)
        match msg := cb.message:
            case types.Message():
                await msg.answer("Choose a type of skin", reply_markup=reply_markup)
            case _:
                print("Message to be answered is inaccessible or missing")


@router.callback_query(F.data == "back_to_skin_slider", ShopState.ExtSlider)
async def back_to_skin_slider(cb: types.CallbackQuery, state: FSMContext):
    """
    Handles the callback to return to the skin slider.

    Changes the FSM state back to the SkinSlider state and deletes the current message.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        state (FSMContext): The current FSM state of the user.
    """

    await state.set_state(ShopState.SkinSlider)
    match cb.message:
        case types.Message():
            await cb.message.delete()
        case _:
            print("Message to be deleted is inaccessible or missing")
