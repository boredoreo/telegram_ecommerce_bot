#TO-DO
# Add function to take vendor's account nuber and  bank immediately after registration
#Add fnctions to edit vendor profile
#Add funtion to view Vendor stats and sales



import logging, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackQueryHandler, CommandHandler,  Filters, Updater, ConversationHandler, MessageHandler
from telegram.files.inputmedia import InputMediaPhoto
from new_models import User, Vendor, Student, Product


current_user = User()
current_product = Product()

def add_product(update,bot):
    current_product = Product()
    bot.bot.send_message(
        chat_id = update.effective_chat.id,
        text='''
        Enter the name of your product name, and price separated by a  comma
        eg 
        <Potato,1000>
        \n**Don't add a hashtag(#) or an 'N' to indicate currency, numbers only
        '''
    )
    return 0

def add_product_description(update, bot):
    name, price = update.message.text.split(',')
    current_product.name = name
    current_product.price = int(price)
    current_product.vendorID =update.effective_chat.id
    bot.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Please send a short description of the meal you wish to add =>"
    )
    return 1

def add_product_picture(update, bot):
    description = update.message.text
    current_product.description = description
    bot.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Please send a picture of the meal you wish to add =>"

    )
    return 2

def add_product_finish(update,bot):
    file_name = "{}.jpg".format(current_product.name)
    file = bot.bot.get_file(update.message.photo[-1].file_id)
    file.download(file_name)
    
    print(current_product.name)
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            current_product.image = f.read()
        current_product.commit()
        os.remove(file_name)
        bot.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Product added successfully"

        )

        return 3
    

def view_products(update,bot):
    images = current_product.get_my_all(myid=update.effective_user.id)
    image = images[0]
    with open(image[1]+".jpg", 'wb') as f:
        f.write(image[2])

    reply_keyboard = [
        [
            InlineKeyboardButton(text="Next", callback_data="view_product_2")
        ],
        [
            InlineKeyboardButton(text="Edit", callback_data="edit_product_{}".format(image[0])),
            InlineKeyboardButton(text="Delete",  callback_data="delete_product")
        ]
    ]

    mark_up = InlineKeyboardMarkup(reply_keyboard)
    

    bot.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo = open(image[1]+".jpg", "rb"),
        caption= '''
        \n{}
        \n{}

        from {}
        '''.format(image[1], image[3], image[4]),
        reply_markup = mark_up
    )
    os.remove(image[1]+".jpg")
    

def view_products_extended(update, bot):
    query = update.callback_query
    state = int(update.callback_query.data[13:])
    images = current_product.get_my_all(myid=update.effective_user.id)
    image = images[state-1]
    with open(image[1]+".jpg", 'wb') as f:
        f.write(image[2])

    if state == len(images):
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Previous", callback_data="view_product_{}".format(state-1))
            ],
            [
                InlineKeyboardButton(text="Edit", callback_data="edit_product_{}".format(image[0])),
                InlineKeyboardButton(text="Delete",  callback_data="delete_product")
            ]
        ]
    elif state == 1:
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Next", callback_data="view_product_{}".format(state+1))
            ],
            [
                InlineKeyboardButton(text="Edit", callback_data="edit_product_{}".format(image[0])),
                InlineKeyboardButton(text="Delete",  callback_data="delete_product")
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
                InlineKeyboardButton(text="Delete",  callback_data="delete_product")
            ]
        ]



    mark_up = InlineKeyboardMarkup(reply_keyboard)
    

    query.message.edit_media(
        InputMediaPhoto(
            media=open(image[1]+".jpg", "rb"),
            caption= '''\n{}\n{}
            from {}
            '''.format(image[1], image[3], image[4]),
            ),
        
        reply_markup = mark_up
    )
    os.remove(image[1]+".jpg")
    print(state)
    return 0
    
def edit_product(update, bot):
    query = update.callback_query
    product_id = query.data[13:]
    current_product=Product()
    current_product.instance=product_id


    bot.bot.send_message(
        chat_id=update.effective_chat.id,
        text='''
        Enter the name of your product name, and price separated by a  comma
        eg 
        <Potato,1000>
        \n**Don't add a hashtag(#) or an 'N' to indicate currency, numbers only
        '''
    )
    return 0

def edit_product_finish(update,bot):
    query = update.callback_query
    product_id = query.data[13:]
    current_product=Product()
    current_product.instance=product_id
    file_name = "{}.jpg".format(current_product.name)
    file = bot.bot.get_file(update.message.photo[-1].file_id)
    file.download(file_name)
    print(current_product.name, current_product.description, current_product.price, current_product.instance)
    
    print(current_product.name)
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            current_product.image = f.read()
        current_product.edit(current_product.name,current_product.image, current_product.description, current_product.price, current_product.instance)
        os.remove(file_name)

    return