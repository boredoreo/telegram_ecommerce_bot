import logging, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackQueryHandler, CommandHandler,  Filters, Updater, ConversationHandler, MessageHandler
from telegram.files.inputmedia import InputMediaPhoto
from database.models import User, Vendor, Student, Product
from database.manipulate import img_to_blob, commit_product




def add_product(update,bot):

    bot.bot.send_message(
        chat_id = update.effective_chat.id,
        text='''
        Enter the name of your product, and price separated by a  comma
        eg 
        <Potato,1000>
        \n**Don't add a hashtag(#) or an 'N' to indicate currency, numbers only
        '''
    )
    return 0

def add_product_description(update, bot):
    name, price = update.message.text.split(',')
    bot.user_data["product"] = Product(
        name=name,
        price=int(price),
        vendorID=update.effective_chat.id
    )
    bot.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Please send a short description of the meal you wish to add =>"
    )
    return 1

def add_product_picture(update, bot):
    description = update.message.text
    current_product  = bot.user_data["product"]
    current_product.description = description
    bot.user_data["product"] = current_product
    bot.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Please send a picture of the meal you wish to add =>"

    )
    return 2


def add_product_finish(update,bot):
    current_product = bot.user_data["product"]
    file_name = "{}.jpg".format(current_product.name)
    file = bot.bot.get_file(update.message.photo[-1].file_id)
    file.download(file_name)

    current_product.image = img_to_blob(img=file_name)
    commit_product(current_product)
    print(current_product.name)
    bot.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Product added successfully"

        )        

    return ConversationHandler.END


add_product_handler = ConversationHandler(
        entry_points=[CommandHandler("add_product", add_product,run_async=True)],
        states={
            0:[MessageHandler(Filters.all, add_product_description,run_async=True)],
            1:[MessageHandler(Filters.all, add_product_picture,run_async=True)],
            2:[MessageHandler(Filters.all, add_product_finish, )],
            
            
        },
        fallbacks=[CommandHandler("add_product", add_product,run_async=True)]
    )