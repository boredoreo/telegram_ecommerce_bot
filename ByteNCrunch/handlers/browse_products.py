import logging, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackQueryHandler, CommandHandler,  Filters, Updater, ConversationHandler, MessageHandler
from telegram.files.inputmedia import InputMediaPhoto
from database.models import  Vendor, Student, Product
from database.manipulate import load_blob
from database.query import get_all_vendors, get_my_products

def browse_product(update,bot):
    vend = (update.callback_query.data)[6:]
    products = get_my_products(vend)
    product = products[0]
    bot.user_data["products"] = products
    file_name = product[1]+".jpg"
    
    image = product[2]
    load_blob(blob=image, file_name=file_name)
    reply_keyboard = [
        [
            InlineKeyboardButton(text="Next", callback_data="browse_product_1")
        ],
        [
            InlineKeyboardButton(text="Add to Cart", callback_data="add_to_cart_{}".format(product[0])),
        ]
    ]

    mark_up = InlineKeyboardMarkup(reply_keyboard)
    

    bot.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo = open(file_name, "rb"),
        caption= '''
        \n{}
        \n{}
        '''.format(product[2],product[3]),
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

    if state == len(products_list):
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


browse_product_handler = CallbackQueryHandler(pattern="visit_", callback= browse_product,run_async=True)
browse_product_ext_handler = CallbackQueryHandler(callback=browse_product_extended, pattern="browse_product_", run_async=True)