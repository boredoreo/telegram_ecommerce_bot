import logging, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackQueryHandler, CommandHandler,  Filters, Updater, ConversationHandler, MessageHandler
from telegram.files.inputmedia import InputMediaPhoto
from database.models import  Vendor, Student, Product
from database.manipulate import load_blob
from database.query import get_all_vendors

#TODO
'''
*add funtion to fetch product data before sending to browse product handler
*integrate with ibiang's api
'''
def browse_vendors(update,bot):
    my_vendors = get_all_vendors()
    vend = my_vendors[0]
    file_name = vend[1]+".jpg"
    image = vend[-1]
    load_blob(blob=image, file_name=file_name)
    reply_keyboard = [
        [
            InlineKeyboardButton(text="Next", callback_data="browse_vendor_2")
        ],
        [
            InlineKeyboardButton(text="Visit", callback_data="visit_{}".format(vend[0])),
        ]
    ]

    mark_up = InlineKeyboardMarkup(reply_keyboard)
    

    bot.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo = open(file_name, "rb"),
        caption= '''
        \n{}
        '''.format(vend[2]),
        reply_markup = mark_up
    )
    os.remove(file_name)
    


def browse_vendors_extended(update,bot):
    query = update.callback_query
    state = int(update.callback_query.data[14:])
    my_vendors = get_all_vendors()
    vend = my_vendors[state-1]
    file_name = vend[1]+".jpg"
    image = vend[-1]
    load_blob(blob=image, file_name=file_name)

    if state == len(my_vendors):
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Previous", callback_data="browse_vendor_{}".format(state-1))
            ],
            [
            InlineKeyboardButton(text="Visit", callback_data="visit_{}".format(vend[0])),
            ]
        ]
    elif state == 1:
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Next", callback_data="browse_vendor_{}".format(state+1))
            ],
            [
            InlineKeyboardButton(text="Visit", callback_data="visit_{}".format(vend[0])),
            ]
        ]
    else:
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Previous", callback_data="browse_vendor_{}".format(state-1)),
                InlineKeyboardButton(text="Next", callback_data="browse_vendor_{}".format(state+1))
            ],
            [
            InlineKeyboardButton(text="Visit", callback_data="visit_{}".format(vend[0])),
            ]
        ]



    mark_up = InlineKeyboardMarkup(reply_keyboard)
    

    query.message.edit_media(
        InputMediaPhoto(
            media= open(file_name, "rb"),
        caption= '''
        \n{}

        '''.format(vend[2])
            ),
        
        reply_markup = mark_up
    )
    os.remove(file_name)
    print(state)
    return 0


browse_vendor_handler = CommandHandler("browse_stores", browse_vendors,run_async=True)
browse_vendor_ext_handler = CallbackQueryHandler(callback=browse_vendors_extended, pattern="browse_vendor_", run_async=True)