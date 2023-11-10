import logging, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackQueryHandler, CommandHandler,  Filters, Updater, ConversationHandler, MessageHandler
from telegram.files.inputmedia import InputMediaPhoto
from database.models import User, Vendor, Student, Product
from database.manipulate import img_to_blob, commit_product, load_blob
from database.query import get_my_products


def view_products(update,bot):
    images = get_my_products(myid=update.effective_user.id)
    image = images[0]
    file_name = image[1]+".jpg"
    load_blob(blob=image[2], file_name=file_name)

    reply_keyboard = [
        [
            InlineKeyboardButton(text="Next", callback_data="view_product_2")
        ],
        [
            InlineKeyboardButton(text="Edit", callback_data="edit_product_{}".format(image[0])),
            InlineKeyboardButton(text="Delete",  callback_data="delete_product_{}".format(image[0]))
        ]
    ]

    mark_up = InlineKeyboardMarkup(reply_keyboard)
    

    bot.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo = open(file_name, "rb"),
        caption= '''
        \n{}
        \n{}

        from {}
        '''.format(image[1], image[3], image[4]),
        reply_markup = mark_up
    )
    os.remove(file_name)

def view_products_extended(update, bot):
    query = update.callback_query
    state = int(update.callback_query.data[13:])
    images =get_my_products(myid=update.effective_user.id)
    image = images[state-1]
    file_name = image[1]+".jpg"
    load_blob(blob=image[2], file_name=file_name)

    if state == len(images):
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Previous", callback_data="view_product_{}".format(state-1))
            ],
            [
                InlineKeyboardButton(text="Edit", callback_data="edit_product_{}".format(image[0])),
                InlineKeyboardButton(text="Delete",  callback_data="delete_product_{}".format(image[0]))
            ]
        ]
    elif state == 1:
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Next", callback_data="view_product_{}".format(state+1))
            ],
            [
                InlineKeyboardButton(text="Edit", callback_data="edit_product_{}".format(image[0])),
                InlineKeyboardButton(text="Delete",  callback_data="delete_product_{}".format(image[0]))
            ]
        ]
    else:
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Previous", callback_data="view_product_{}".format(state-1)),
                InlineKeyboardButton(text="Next", callback_data="view_product_{}".format(state+1))
            ],
            [
                InlineKeyboardButton(text="Edit", callback_data="edit_product_{}".format(image[0])),
                InlineKeyboardButton(text="Delete",  callback_data="delete_product_{}".format(image[0]))
            ]
        ]



    mark_up = InlineKeyboardMarkup(reply_keyboard)
    

    query.message.edit_media(
        InputMediaPhoto(
            media=open(file_name, "rb"),
            caption= '''\n{}\n{}
            from {}
            '''.format(image[1], image[3], image[4]),
            ),
        
        reply_markup = mark_up
    )
    os.remove(file_name)
    print(state)
    return 


view_products_handler = CommandHandler("view_products", view_products)

view_products_ext_handler = CallbackQueryHandler(pattern="view_product_", callback=view_products_extended)