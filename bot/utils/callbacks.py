from aiogram.filters.callback_data import CallbackData


class CategoryCallback(CallbackData, prefix="category"):
    """
    Callback data for category selection in the bot interface (e.g., Rifles, Pistols).

    Attributes:
        id (int): The unique identifier for the category.
        action (str): The action to be performed with this category (e.g., view, select).
    """

    id: int
    action: str


class SubCategoryCallback(CallbackData, prefix="sub_cat"):
    """
    Callback data for sub-category selection (e.g., AK-47, AWP).

    Attributes:
        id (int): The unique identifier for the sub-category.
        action (str): The action associated with this sub-category.
    """

    id: int
    action: str


class SkinCallback(CallbackData, prefix="skin"):
    """
    Callback data for skin selection (e.g., AK-47 | Ice-Coaled).

    Attributes:
        id (int): The unique identifier for the skin.
        action (str): The action to perform related to the skin.
    """

    id: int
    action: str


class ExtCallback(CallbackData, prefix="exterior"):
    """
    Callback data for exterior selection (e.g., Minimal Wear, Field-Tested).

    Attributes:
        name (str): The name of the exterior type.
        action (str): The action associated with this exterior type.
    """

    name: str
    action: str


class SkinTypeCallback(CallbackData, prefix="skin_type"):
    """
    Callback data for skin type selection (e.g., Basic, Souvenir, StatTrack).

    Attributes:
        name (str): The type of the skin.
        price (float): The price associated with the skin type.
        action (str): The action related to the skin type.
    """

    name: str
    price: float
    action: str


class PaymentCallback(CallbackData, prefix="payment"):
    """
    Callback data for payment method selection (e.g., Sber, PayMaster).

    Attributes:
        method (str): The payment method (e.g., Sber, PayMaster).
        action (str): The action associated with the payment method.
    """

    method: str
    action: str
