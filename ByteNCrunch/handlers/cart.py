from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackQueryHandler
from database.query import get_product


def add_to_cart(update, bot):
    query = update.callback_query
    data = update.callback_query.data
    match data[:13]:
        #anything to dodge regex, lol
        case "cart_quan_add":
            product_id = update.callback_query.data[18:]
            print(product_id)
            product = get_product(product_id)
            product_count = bot.user_data["product_count"] 
            product_count +=1
            bot.user_data["product_count"] = product_count
        case "cart_quan_min":
            if product > 1:
                product_id = update.callback_query.data[20:]
                product = get_product(product_id)
                product_count = bot.user_data["product_count"]
                product_count -=1
                bot.user_data["product_count"] = product_count
            else:
                product_id = update.callback_query.data[20:]
                product = get_product(product_id)
                product_count = 1
                bot.user_data["product_count"] = product_count

        case _:
            product_id = update.callback_query.data[12:]
            product = get_product(product_id)
            product_count = 1
            bot.user_data["product_count"] = product_count
    
    reply_keyboard = [
        [
            InlineKeyboardButton(text="-1", callback_data=f"cart_quan_minus_one_{product_id}"),
            InlineKeyboardButton(text="+1", callback_data=f"cart_quan_add_one_{product_id}")
        ],
        [
            InlineKeyboardButton(text="Add to cart", callback_data=f"add_to_cart_{product_id}_{product_count}")
        ],
        [
            InlineKeyboardButton(text="Cancel", callback_data="start")
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text=f"Add {product[1]} to cart?  \nQuantity : {product_count} \nPrice : # {int(product[3] * product_count)}",
        reply_markup=markup,
    )

def add_to_cart_confirm(update, bot):
    query = update.callback_query
    data = update.callback_query.data
    product_id = int(data[12:].split("_")[0])
    product_count = int(data[12:].split("_")[1])
    bot.user_data["cart"][product_id] = product_count
    bot.user_data["cart_total"] += product_count * get_product(product_id)[3]
    print(get_product(product_id)[3])
    reply_keyboard = [
        
        [
            InlineKeyboardButton(text="Proceed to Checkout", callback_data="checkout")
        ] ,
         [
            InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
        ] ,
        [
            InlineKeyboardButton(text="Back to Home!", callback_data="start")
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text=f"{product_count} units of {get_product(product_id)[1] }added to cart! \n To proceed to checkout, tap on 'Manage Cart'",
        reply_markup=markup,
    )


def manage_cart(update, bot):
    cart = list(bot.user_data["cart"].items())
    query = update.callback_query
    my_text = "Here's what you have in your cart right now!"
    for i in cart:
        product = get_product(i[0])
        my_text += f"\n >> {i[1]} orders of {product[1]} at # {int(product[3]) * i[1]}"

    
    reply_keyboard = [
        
        [
             InlineKeyboardButton(text="edit", callback_data="edit"),
            InlineKeyboardButton(text="Proceed to Checkout", callback_data="checkout")
        ]

    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text=my_text,
        reply_markup=markup,
    )

    

    
add_to_cart_handler = CallbackQueryHandler(callback=add_to_cart, pattern="add_product_", run_async=True )
cart_quantity_handler = CallbackQueryHandler(callback=add_to_cart, pattern="cart_quan_", run_async=True)
confirm_cart = CallbackQueryHandler(callback=add_to_cart_confirm, pattern="add_to_cart_")
manage_cart_handler = CallbackQueryHandler(callback=manage_cart, pattern="manage_cart")
