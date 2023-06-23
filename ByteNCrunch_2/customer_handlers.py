import logging, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackQueryHandler, CommandHandler,  Filters, Updater, ConversationHandler, MessageHandler
from telegram.files.inputmedia import InputMediaPhoto
from new_models import User, Vendor, Student, Product


current_user = User()
current_product = Product()
vendor = Vendor()
def search(update, bot):
    pass

def browse_vendors(update,bot):
    my_vendors = vendor.get_all()
    vend = my_vendors[0]
    image = vend[-1]
    with open(vend[1]+".jpg", 'wb') as f:
        f.write(image)

    reply_keyboard = [
        [
            InlineKeyboardButton(text="Next", callback_data="browse_vendor_2")
        ],
        [
            InlineKeyboardButton(text="Edit", callback_data="edit_product_{}".format(image[0])),
            InlineKeyboardButton(text="Delete",  callback_data="delete_product")
        ]
    ]

    mark_up = InlineKeyboardMarkup(reply_keyboard)
    

    bot.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo = open(vend[1]+".jpg", "rb"),
        caption= '''
        \n{}
        
        '''.format(vend[2]),
        reply_markup = mark_up
    )
    os.remove(vend[1]+".jpg")
    


def browse_vendors_extended(update,bot):
    query = update.callback_query
    state = int(update.callback_query.data[14:])
    my_vendors = vendor.get_all()
    vend = my_vendors[state-1]
    image = vend[-1]
    with open(vend[1]+".jpg", 'wb') as f:
        f.write(image)

    if state is len(my_vendors):
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Previous", callback_data="browse_vendor_{}".format(state-1))
            ],
            [
                InlineKeyboardButton(text="Edit", callback_data="edit_product_{}".format(image[0])),
                InlineKeyboardButton(text="Delete",  callback_data="delete_product")
            ]
        ]
    elif state is 1:
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Next", callback_data="browse_vendor_{}".format(state+1))
            ],
            [
                InlineKeyboardButton(text="Edit", callback_data="edit_product_{}".format(image[0])),
                InlineKeyboardButton(text="Delete",  callback_data="delete_product")
            ]
        ]
    else:
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Previous", callback_data="browse_vendor_{}".format(state-1)),
                InlineKeyboardButton(text="Next", callback_data="browse_vendor_{}".format(state+1))
            ],
            [
                InlineKeyboardButton(text="Edit", callback_data="edit_product_{}".format(image[0])),
                InlineKeyboardButton(text="Delete",  callback_data="delete_product")
            ]
        ]



    mark_up = InlineKeyboardMarkup(reply_keyboard)
    

    query.message.edit_media(
        InputMediaPhoto(
            media= open(vend[1]+".jpg", "rb"),
        caption= '''
        \n{}

        '''.format(vend[2])
            ),
        
        reply_markup = mark_up
    )
    os.remove(vend[1]+".jpg")
    print(state)
    return 0

def add_to_cart(update,bot):
    pass

def check_out(update,bot):
    pass

def view_cart(update,bot):
    pass

def view_cart_extend(update,bot):
    pass

def edit_cart_item(update,bot):
    pass

def pay(update,bot):
    pass