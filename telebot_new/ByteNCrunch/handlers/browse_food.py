from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackQueryHandler
from database.query import get_all_vendors, get_products_from, get_product


# *add funtion to fetch product data before sending to browse product handler
# *integrate with ibiang's api

def browse_product(update, bot):
    vend = ((update.callback_query.data)[12:])
    products = get_products_from(vend)
    print(products)
    bot.user_data["products"] = products
    browse_state = 5
    bot.user_data["browse_state"] = browse_state
    my_products = products[0:browse_state]
    buttons = []
    for food in my_products:
        buttons.append(
            [InlineKeyboardButton(text=food[1], callback_data=f"add_product_{food[0]}")]
        )
    reply_keyboard = buttons + [
            [
                InlineKeyboardButton(text="Next", callback_data="browse_products_next"),
                InlineKeyboardButton(text="Previous", callback_data="browse_products_previous")
            ],
            [
                InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
            ]
        
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    bot.bot.send_message(
        chat_id=update.effective_chat.id,
        text="What do you feel like getting today?",
        reply_markup=markup,
    )

def add_product_extended(update,bot):
    query = update.callback_query
    match update.callback_query.data:
        case "browse_products_next":
            state = bot.user_data["browse_state"]
            my_products = bot.user_data["products"][state:state+5]
            bot.user_data["browse_state"] = state + 5
            buttons = []
            for food in my_products:
                buttons.append(
                    [InlineKeyboardButton(text=food[1], callback_data=f"add_product_{food[0]}")]
                )
            reply_keyboard =buttons + [
                 
                    [
                        InlineKeyboardButton(text="Next", callback_data="browse_products_next"),
                        InlineKeyboardButton(text="Previous", callback_data="browse_products_previous")
                    ],
                    [
                        InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
                    ]
                
            ]
            
            
        case "browse_products_previous":
            state = bot.user_data["browse_state"]
            if state > 5:
                state = bot.user_data["browse_state"]
                my_products = bot.user_data["products"][state-10:state-5]
                bot.user_data["browse_state"] = state - 5
                buttons = []
                for food in my_products:
                    buttons.append(
                        [InlineKeyboardButton(text=food[1], callback_data=f"add_product_{food[0]}")]
                    )
                reply_keyboard = buttons + [
                        [
                            InlineKeyboardButton(text="Next", callback_data="browse_products_next"),
                            InlineKeyboardButton(text="Previous", callback_data="browse_products_previous")
                        ],
                        [
                            InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
                        ]
                    
                ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text="What do you feel like getting today?",
        reply_markup=markup,
    )

def add_to_cart(update, bot):
    query = update.callback_query
    product_id = update.callback_query.data[12:]
    product = get_product(product_id)
    reply_keyboard = [
        [
            InlineKeyboardButton(text="Add to cart", callback_data="add_to_cart")
        ],
        [
            InlineKeyboardButton(text="Cancel", callback_data="cancel")
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    bot.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Confirm adding ",
        reply_markup=markup,
    )

add_product_handler = CallbackQueryHandler(pattern="browse_shop_", callback= browse_product,run_async=True)
add_product_ext_handler = CallbackQueryHandler(callback=add_product_extended, pattern="browse_products_", run_async=True)