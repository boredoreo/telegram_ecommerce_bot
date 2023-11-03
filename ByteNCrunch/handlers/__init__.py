from .cart import add_to_cart_handler
from .start_up import start_handler
from .search import search_handler
from .add_products import add_product_handler
from .view_products import view_products_handler, view_products_ext_handler
from .browse_vendors import browse_vendor_handler, browse_vendor_ext_handler
from .edit_product_hand import edit_product_handler, delete_product_handler
from .browse_products import browse_product_handler, browse_product_ext_handler
from .complaint import complaint_handler

all_handlers = [
    start_handler,
    add_product_handler,
    view_products_handler,
    view_products_ext_handler,
    browse_vendor_handler,
    browse_vendor_ext_handler,
    edit_product_handler,
    delete_product_handler,
    browse_product_handler,
    browse_product_ext_handler,
    search_handler,
    complaint_handler
]