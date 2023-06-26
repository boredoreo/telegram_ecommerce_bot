from .start_up import start_handler
from .add_products import add_product_handler
from .view_products import view_products_handler, view_products_ext_handler
from .browse_vendors import browse_vendor_handler, browse_vendor_ext_handler

all_handlers = [
    start_handler,
    add_product_handler,
    view_products_handler,
    view_products_ext_handler,
    browse_vendor_handler,
    browse_vendor_ext_handler
]