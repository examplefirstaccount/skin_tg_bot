"""The file contains handlers for Ext slider (list of exteriors for skin)"""


from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown as fmt
from aiogram.types.input_media_photo import InputMediaPhoto

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.data.config import LG_EXTERIORS
from bot.db.models import Skin, Exterior as Ext
from bot.states import ShopState
from bot.utils.api.skins import get_ext_images, get_ext_prices
from bot.utils.callbacks import ExtCallback
from bot.keyboards.inline import get_ext_slider_menu, get_payment_methods, get_skin_types

router = Router(name='exterior_slider')


def get_ext_caption(
        skin_name: str,
        skin_type: str,
        ext: str,
        price: float,
        spec_price: float
) -> str:

    name = f'{skin_name} ({ext})' if ext != 'none' else skin_name
    if skin_type == 'Normal':
        price = fmt.text(fmt.hbold('Price: '), fmt.hitalic('$', price))
    else:
        # 4 spaces for italic or code, 7 space for bold
        price = fmt.text(fmt.hbold('Basic:       '), fmt.hitalic('$', price), '\n', '\n',
                         fmt.hbold(f'{skin_type}: '), fmt.hitalic('$', spec_price),
                         sep=''
                         )
    return fmt.text(
        fmt.hcode(name), '\n', '\n',
        price, '\n', '\n',
        sep=''
    )


async def get_ext_data(
        session: AsyncSession,
        skin_id: int
) -> tuple:

    sql_query = select(Skin.name, Skin.type, Skin.category_id).filter_by(id=skin_id)
    result = await session.execute(sql_query)
    skin_name, skin_type, cat_id = result.first()

    sql_query = select(Ext.ext, Ext.price_id, Ext.spec_price_id).filter_by(skin_id=skin_id)
    result = await session.execute(sql_query)
    ext_data = result.all()

    if cat_id in [1, 2]:
        skin_name = '★ ' + skin_name
    skin_ext, skin_price_ids, skin_spec_price_ids = zip(*ext_data)
    images = get_ext_images(skin_name)
    prices = get_ext_prices(list(skin_price_ids + skin_spec_price_ids))

    result = []
    for i in range(len(skin_ext)):
        ext = LG_EXTERIORS[skin_ext[i]] if skin_ext[i] != 'none' else 'none'
        price_id = skin_price_ids[i]
        spec_price_id = skin_spec_price_ids[i]
        price = prices[price_id] if price_id and price_id in prices else '-'

        if skin_type == 'Normal':
            spec_price = '-'
        else:
            spec_price = prices[spec_price_id] if spec_price_id and spec_price_id in prices else '-'

        if ext == 'none':
            img = list(images.values())[0]
            result.append({'ext_name': ext, 'img': img, 'price': price, 'spec_price': spec_price})
            return result, skin_type, skin_name.replace('★ ', '')
        else:
            img = images[ext] if ext in images else None

        result.append({'ext_name': ext, 'img': img, 'price': price, 'spec_price': spec_price})

    return result, skin_type, skin_name.replace('★ ', '')


async def start_ext_slider(
        cb: types.CallbackQuery,
        session: AsyncSession,
        skin_id: int,
        start_i: int
) -> dict:

    ext_data, skin_type, skin_name = await get_ext_data(session, skin_id)
    slider = {'ext_data': ext_data, 'skin_type': skin_type, 'skin_name': skin_name,
              'ext_count': len(ext_data), 'pos': start_i}

    photo = ext_data[start_i]['img']
    caption = get_ext_caption(skin_name=skin_name,
                              skin_type=skin_type,
                              ext=ext_data[start_i]['ext_name'],
                              price=ext_data[start_i]['price'],
                              spec_price=ext_data[start_i]['spec_price']
                              )
    reply_markup = get_ext_slider_menu(skin_ext=ext_data[start_i]['ext_name'],
                                       curr_pos=start_i + 1,
                                       skins_count=slider['ext_count']
                                       )

    await cb.message.answer_photo(photo=photo, caption=caption, reply_markup=reply_markup)

    return slider


@router.callback_query(F.data.regexp(r'(prev|next)_ext'), ShopState.ExtSlider)
async def update_slider(
        cb: types.CallbackQuery,
        state: FSMContext
):

    state_data = await state.get_data()
    slider = state_data['ext_slider']

    ext_data = slider['ext_data']
    past_i = slider['pos']

    if cb.data == 'prev_ext':
        curr_i = past_i - 1 if past_i != 0 else slider['ext_count'] - 1
    else:
        curr_i = past_i + 1 if past_i != slider['ext_count'] - 1 else 0

    if curr_i == past_i:
        pass
    else:
        slider['pos'] = curr_i
        caption = get_ext_caption(skin_name=slider['skin_name'],
                                  skin_type=slider['skin_type'],
                                  ext=ext_data[curr_i]['ext_name'],
                                  price=ext_data[curr_i]['price'],
                                  spec_price=ext_data[curr_i]['spec_price']
                                  )
        reply_markup = get_ext_slider_menu(skin_ext=ext_data[curr_i]['ext_name'],
                                           curr_pos=curr_i + 1,
                                           skins_count=slider['ext_count']
                                           )
        media = InputMediaPhoto(media=ext_data[curr_i]['img'], caption=caption)

        await state.update_data(ext_slider=slider)
        await cb.message.edit_media(media=media)
        await cb.message.edit_reply_markup(reply_markup=reply_markup)


@router.callback_query(ExtCallback.filter(F.action == 'buy'), ShopState.ExtSlider)
async def buy_skin(
        cb: types.CallbackQuery,
        state: FSMContext,
):

    state_data = await state.get_data()
    slider = state_data['ext_slider']

    ext_data = slider['ext_data']
    skin_name = slider['skin_name']
    skin_type = slider['skin_type']
    pos = slider['pos']

    ext = ext_data[pos]['ext_name']
    price = ext_data[pos]['price']
    spec_price = ext_data[pos]['spec_price']

    buy_title = f'{skin_name} ({ext})' if ext != 'none' else skin_name

    await state.update_data(buy_title=buy_title)

    if skin_type == 'Normal' or ((price == '-') ^ (spec_price == '-')):
        buy_type = 'Basic' if spec_price == '-' else skin_type
        buy_price = price if spec_price == '-' else spec_price

        await state.update_data(buy_type=buy_type, buy_price=buy_price, skipped_skin_type_choosing=True)
        await state.set_state(ShopState.ChoosePaymentMethod)
        await cb.message.answer('Choose payment method', reply_markup=get_payment_methods())
    else:
        reply_markup = get_skin_types(['Basic', price], [skin_type, spec_price])

        await state.set_state(ShopState.ChooseSkinType)
        await cb.message.answer('Choose a type of skin', reply_markup=reply_markup)


@router.callback_query(F.data == 'back_to_skin_slider', ShopState.ExtSlider)
async def back_to_skin_slider(
        cb: types.CallbackQuery,
        state: FSMContext
):

    await state.set_state(ShopState.SkinSlider)
    await cb.message.delete()
