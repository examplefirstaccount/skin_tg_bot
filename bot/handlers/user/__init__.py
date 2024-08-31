"""Handlers for ordinary users"""

from .callbacks.catalog import router as category_router
from .callbacks.category_page import router as sub_cat_router
from .callbacks.ext_slider import router as ext_router
from .callbacks.skins_slider import router as skin_router
from .commands.help import router as help_router
from .commands.shop import router as shop_router
from .commands.start import router as start_router
from .payment import router as payment_router
from .pre_invoice_process import router as pre_inv_router

user_routers = (
    start_router,
    help_router,
    shop_router,
    category_router,
    sub_cat_router,
    skin_router,
    ext_router,
    pre_inv_router,
    payment_router,
)
