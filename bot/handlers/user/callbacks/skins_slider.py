"""
Handlers for the Skin slider (list of skins for an item).

Handlers:
    - update_skin_slider: Handles navigation through the skin slider (next/previous).
    - show_skin: Initiates the exterior slider for the selected skin.
    - back_to_sub_cat_page: Handles the callback to return to the sub-category page.
Utilities:
    - get_skin_caption: Generates a formatted caption for the skin slider.
    - get_skins_data: Retrieves data for the skin slider, including images and descriptions.
    - start_skin_slider: Initializes the skin slider with the first skin in the list.
"""

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown as fmt
from aiogram.types.input_media_photo import InputMediaPhoto

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Skin
from bot.states import ShopState
from bot.utils.callbacks import SkinCallback
from bot.handlers.user.callbacks.ext_slider import start_ext_slider
from bot.keyboards.inline import get_skin_slider_menu

router = Router(name='skin_slider')


def get_skin_caption(skin_name: str, skin_descr: str) -> str:
    """
    Generates a formatted caption for the skin slider.

    Formats the caption using the skin's name and a brief description.

    Args:
        skin_name (str): The name of the skin.
        skin_descr (str): A description of the skin.

    Returns:
        str: A formatted string for the caption.
    """
    return fmt.text(
        fmt.hcode(skin_name), '\n', '\n',
        skin_descr.split('.')[0] + '.', '\n', '\n',
        sep=''
    )


async def get_skins_data(
        session: AsyncSession,
        sub_cat_id: int
) -> tuple:
    """
    Retrieves data for the skin slider, including images and descriptions.

    Queries the database for skins under a specific sub-category and gathers
    their IDs, names, images, and descriptions.

    Args:
        session (AsyncSession): The database session for executing queries.
        sub_cat_id (int): The ID of the sub-category to fetch skins for.

    Returns:
        tuple: A tuple containing lists of skin IDs, names, images, descriptions, and the total count of skins.
    """

    sql_query = select(Skin.id, Skin.name,
                       Skin.img, Skin.descr).filter_by(sub_category_id=sub_cat_id).order_by(Skin.id)
    result = await session.execute(sql_query)
    skins_data = result.all()

    skin_ids, skin_names, skin_images, skins_descr = zip(*skins_data)
    skin_count = len(skins_data)

    return skin_ids, skin_names, skin_images, skins_descr, skin_count


async def start_skin_slider(
        cb: types.CallbackQuery,
        session: AsyncSession,
        sub_cat_id: int,
        start_i: int
) -> dict:
    """
    Initializes the skin slider with the first skin in the list.

    Fetches skin data and displays the first skin with its image, caption, and slider menu.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        session (AsyncSession): The database session for querying skins.
        sub_cat_id (int): The ID of the sub-category to display skins for.
        start_i (int): The starting index for the slider (typically 0).

    Returns:
        dict: A dictionary containing slider data including skin details and the current position.
    """

    skin_ids, skin_names, skin_images, skins_descr, skin_count = await get_skins_data(session, sub_cat_id)
    slider = {
        'skin_ids': skin_ids,
        'skin_names': skin_names,
        'skin_images': skin_images,
        'skins_descr': skins_descr,
        'skin_count': skin_count,
        'sub_cat_id': sub_cat_id,
        'pos': start_i
    }

    photo = skin_images[start_i]
    caption = get_skin_caption(skin_name=skin_names[start_i], skin_descr=skins_descr[start_i])
    reply_markup = get_skin_slider_menu(
        skin_id=skin_ids[start_i],
        curr_pos=start_i + 1,
        skins_count=skin_count
    )

    await cb.message.answer_photo(photo=photo, caption=caption, reply_markup=reply_markup)

    return slider


@router.callback_query(F.data.regexp(r'(next|prev)_skin'), ShopState.SkinSlider)
async def update_skin_slider(
        cb: types.CallbackQuery,
        state: FSMContext
):
    """
    Handles navigation through the skin slider (next/previous).

    Updates the slider to show the next or previous skin based on user input,
    updating the image, caption, and navigation buttons.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        state (FSMContext): The current FSM state of the user.
    """

    state_data = await state.get_data()
    slider = state_data['skin_slider']

    past_i = slider['pos']

    if cb.data == 'prev_skin':
        curr_i = past_i - 1 if past_i != 0 else slider['skin_count'] - 1
    else:
        curr_i = past_i + 1 if past_i != slider['skin_count'] - 1 else 0

    slider['pos'] = curr_i
    media = InputMediaPhoto(media=slider['skin_images'][curr_i],
                            caption=get_skin_caption(slider['skin_names'][curr_i], slider['skins_descr'][curr_i])
                            )

    reply_markup = get_skin_slider_menu(skin_id=slider['skin_ids'][curr_i],
                                        curr_pos=curr_i + 1,
                                        skins_count=slider['skin_count']
                                        )

    await state.update_data(skin_slider=slider)
    await cb.message.edit_media(media=media)
    await cb.message.edit_reply_markup(reply_markup=reply_markup)


@router.callback_query(SkinCallback.filter(F.action == 'view'), ShopState.SkinSlider)
async def show_skin(
        cb: types.CallbackQuery,
        state: FSMContext,
        callback_data: SkinCallback,
        session: AsyncSession
):
    """
    Handles the transition to viewing specific exteriors of a selected skin.

    Transitions the state to the exterior slider for the selected skin, initializing the slider
    with exteriors for the chosen skin.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        state (FSMContext): The current FSM state of the user.
        callback_data (SkinCallback): The callback data containing the skin ID to view.
        session (AsyncSession): The database session for querying skin details.
    """

    skin_id = callback_data.id

    ext_slider = await start_ext_slider(cb=cb, session=session, skin_id=skin_id, start_i=0)
    await state.update_data(ext_slider=ext_slider)
    await state.set_state(ShopState.ExtSlider)


@router.callback_query(F.data == 'back_to_sub_cat_page', ShopState.SkinSlider)
async def back_to_sub_cat_page(
        cb: types.CallbackQuery,
        state: FSMContext
):
    """
    Handles the callback to return to the sub-category page.

    Changes the FSM state back to the CategoryPage state and deletes the current message.

    Args:
        cb (types.CallbackQuery): The callback query object from the user.
        state (FSMContext): The current FSM state of the user.
    """

    await state.set_state(ShopState.CategoryPage)
    await cb.message.delete()
