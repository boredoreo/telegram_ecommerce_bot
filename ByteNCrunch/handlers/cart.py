import logging, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackQueryHandler, CommandHandler,  Filters, Updater, ConversationHandler, MessageHandler
from telegram.files.inputmedia import InputMediaPhoto
from database.models import  Vendor, Student, Product
from database.manipulate import load_blob
from database.query import get_all_vendors, get_my_products, get_product
# Add something for quantity
# Order Item-- won't work without it
def add_to_cart(update,bot):
    product = get_product(update.callback_query.data[12:])
    cart_list = bot.user_data["cart"] 
    cart_list.append(product)
    bot.user_data["cart"] = cart_list 
    bot.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Item added to cart"
    )

def manage_cart(update,bot):
    cart = bot.user_data["cart"]
    item = cart[0]
    file_name = item[1]+".jpg"
    
    image = item[2]
    load_blob(blob=image, file_name=file_name)
    reply_keyboard = [
        [
            InlineKeyboardButton(text="Next", callback_data="browse_cart_1")
        ],
        [
            InlineKeyboardButton(text="Delete", callback_data="add_to_cart_{}".format(0)),
        ],
        [
            InlineKeyboardButton(text="Checkout", callback_data="checkout"),
        ]
    ]

    mark_up = InlineKeyboardMarkup(reply_keyboard)
    

    bot.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo = open(file_name, "rb"),
        caption= '''
        \n{}
        \n{}
        '''.format(item[2],product[3]),
        reply_markup = mark_up
    )
    os.remove(file_name)
    


def browse_product_extended(update,bot):
    query = update.callback_query
    state = int(update.callback_query.data[15:])
    products_list = bot.user_data["products"]
    current_product = products_list[state]
    # vend = my_vendors[state-1]
    file_name = current_product[1]+".jpg"
    image = current_product[2]
    load_blob(blob=image, file_name=file_name)

    if state == len(my_vendors):
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Previous", callback_data="browse_product_{}".format(state-1))
            ],
            [
            InlineKeyboardButton(text="Add to Cart", callback_data="add_to_cart_{}".format(current_product[0])),
            ]
        ]
    elif state == 1:
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Next", callback_data="browse_product_{}".format(state+1))
            ],
            [
             InlineKeyboardButton(text="Add to Cart", callback_data="add_to_cart_{}".format(current_product[0])),
            ]
        ]
    else:
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Previous", callback_data="browse_product_{}".format(state-1)),
                InlineKeyboardButton(text="Next", callback_data="browse_product_{}".format(state+1))
            ],
            [
             InlineKeyboardButton(text="Add to Cart", callback_data="add_to_cart_{}".format(current_product[0])),
            ]
        ]



    mark_up = InlineKeyboardMarkup(reply_keyboard)
    

    query.message.edit_media(
        InputMediaPhoto(
            media= open(file_name, "rb"),
        caption= '''
        \n{},
        \n{}

        '''.format(current_product[1],current_product[3])
            ),
        
        reply_markup = mark_up
    )
    os.remove(file_name)
    print(state)
    return 0


add_to_cart_handler = CallbackQueryHandler(pattern="add_to_cart_", callback=add_to_cart)