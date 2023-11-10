# from .cart import add_to_cart_handler
from .search import search_handler
from .complaint import complaint_handler
from .start_up import start_handler, setup_user_handler
from .browse_vendors import browse_vendor_handler, browse_vendor_ext_handler
from .browse_products import browse_product_handler, browse_product_ext_handler

all_handlers = [
    # Start up Handlers
    start_handler,
    setup_user_handler,

    # Vendor Handlers
    browse_vendor_handler,
    browse_vendor_ext_handler,

    #complaint
    complaint_handler,
    
    #Product handlers
    browse_product_handler,
    browse_product_ext_handler,
    search_handler
]