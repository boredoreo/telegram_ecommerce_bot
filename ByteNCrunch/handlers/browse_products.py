import logging, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackQueryHandler, CommandHandler,  Filters, Updater, ConversationHandler, MessageHandler
from telegram.files.inputmedia import InputMediaPhoto
from database.models import  Vendor, Student, Product
from database.query import get_all_vendors, get_products_from


'''
*products should be a list of lists
*pruducts should be saved in user data either at the point of searching or when being redirected from vendor browsing
ie products should be fetched prior too getting to this page
'''
def browse_product(update,bot):
    vend = ((update.callback_query.data)[12:])
    products = get_products_from(vend)
    bot.user_data["products"] = products
    product = products[0]
    reply_keyboard = [
        [
            InlineKeyboardButton(text="Next", callback_data="browse_product_1")
        ],
        [
            InlineKeyboardButton(text="Add to Cart", callback_data="add_to_cart_{}".format(product[0])),
            InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")

        ]
    ]

    markup = InlineKeyboardMarkup(reply_keyboard)
    bot.bot.send_message(
        chat_id=update.message.chat_id,
        text= '''
            ###PLACEHOLDER TEXT FOR PRODUCT INFO###
            ''',
        reply_markup=markup,
    )


def browse_product_extended(update,bot):
    query = update.callback_query
    state = int(update.callback_query.data[15:])
    products_list = bot.user_data["products"]
    current_product = products_list[state]

    if state == len(products_list):
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Previous", callback_data="browse_product_{}".format(state-1))
            ],
            [
                InlineKeyboardButton(text="Add to Cart", callback_data="add_to_cart_{}".format(current_product[0])),
                InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")

            ]
        ]
    elif state == 1:
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Next", callback_data="browse_product_{}".format(state+1))
            ],
            [
                InlineKeyboardButton(text="Add to Cart", callback_data="add_to_cart_{}".format(current_product[0])),
                InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
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
                InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
            ]
        ]



    markup = InlineKeyboardMarkup(reply_keyboard)
    query.message.edit_message(
        chat_id=update.message.chat_id,
        text= '''
            ###PLACEHOLDER TEXT FOR PRODUCT INFO###
            ''',
        reply_markup=markup,
    )
    return 0


browse_product_handler = CallbackQueryHandler(pattern="visit_", callback= browse_product,run_async=True)
browse_product_ext_handler = CallbackQueryHandler(callback=browse_product_extended, pattern="browse_product_", run_async=True)