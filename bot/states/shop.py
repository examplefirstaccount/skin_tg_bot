from aiogram.filters.state import StatesGroup, State


class ShopState(StatesGroup):
    """
    Represents different states of the shopping flow in the bot.

    Each state corresponds to a specific part of the user interaction process within the shop,
    guiding the bot's behavior based on the current state.
    """

    Catalog = State()              # State representing the main catalog view.
    CategoryPage = State()         # State when viewing a specific category page.
    SkinSlider = State()           # State when navigating through skins in a slider.
    ExtSlider = State()            # State when navigating through skin exteriors in a slider.
    ChooseSkinType = State()       # State for choosing the type of skin (e.g., Souvenir, StatTrack).
    ChoosePaymentMethod = State()  # State for selecting a payment method.
    Payment = State()              # State for processing the payment.
