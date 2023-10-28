from aiogram.filters.state import StatesGroup, State


class ShopState(StatesGroup):
    Catalog = State()
    CategoryPage = State()
    SkinSlider = State()
    ExtSlider = State()
    ChooseSkinType = State()
    ChoosePaymentMethod = State()
    Payment = State()
