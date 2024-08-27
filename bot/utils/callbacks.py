from aiogram.filters.callback_data import CallbackData


# Rifles, Pistols etc.
class CategoryCallback(CallbackData, prefix='category'):
    id: int
    action: str


# AK-47, AWP etc.
class SubCategoryCallback(CallbackData, prefix='sub_cat'):
    id: int
    action: str


# AK-47 | Ice-Coaled etc.
class SkinCallback(CallbackData, prefix='skin'):
    id: int
    action: str


# Minimal Wear (MW) etc.
class ExtCallback(CallbackData, prefix='exterior'):
    name: str
    action: str


# Basic | Souvenir | StatTrack
class SkinTypeCallback(CallbackData, prefix='skin_type'):
    name: str
    price: float
    action: str


# Sber, PayMaster etc.
class PaymentCallback(CallbackData, prefix='payment'):
    method: str
    action: str
