import logging, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    Updater,
    ConversationHandler,
    MessageHandler,
)
from telegram.files.inputmedia import InputMediaPhoto
from database.models import User, Vendor, Student, Product
from database.manipulate import load_blob, img_to_blob, edit_product, delete_product
from database.query import get_all_vendors, get_product


def edit_product_start(update, bot):
    query = update.callback_query
    product_id = query.data[13:]
    current_product = get_product(product_id)
    bot.user_data["product"] = current_product

    bot.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
        Enter the name of your product name, and price separated by a  comma
        eg 
        <Potato,1000>
        \n**Don't add a hashtag(#) or an 'N' to indicate currency, numbers only
        """,
    )
    return 0


def add_product_description(update, bot):
    name, price = update.message.text.split(",")
    current_product = bot.user_data["product"]
    current_product.name = name
    current_product.price = price
    bot.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please send a short description of the meal you wish to add =>",
    )
    bot.user_data["product"] = current_product
    return 1


def add_product_picture(update, bot):
    description = update.message.text
    current_product = bot.user_data["product"]
    current_product.description = description
    bot.user_data["product"] = current_product
    bot.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please send a picture of the meal you wish to add =>",
    )
    return 2


def edit_product_finish(update, bot):
    query = update.callback_query
    current_product = bot.user_data["product"]
    # product_id=current_product.instance
    file_name = "{}.jpg".format(current_product.name)
    file = bot.bot.get_file(update.message.photo[-1].file_id)
    file.download(file_name)
    print(
        current_product.name,
        current_product.description,
        current_product.price,
        current_product.instance,
    )
    current_product.image = img_to_blob(file_name)
    print(current_product.name)

    edit_product(current_product)

    del bot.user_data["product"]
    return ConversationHandler.END


def delete_product_hand(update,bot):
    query =  update.callback_query
    product_id = query.data[15:]
    print(product_id)
    delete_product(product_id)
    bot.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Product Deleted!"
    )


edit_product_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            pattern="edit_product_", callback=edit_product_start, run_async=True
        )
    ],
    states={
        0: [MessageHandler(Filters.all, add_product_description)],
        1: [MessageHandler(Filters.all, add_product_picture)],
        2: [MessageHandler(Filters.all, edit_product_finish)],
    },
    fallbacks=[],
)

delete_product_handler = CallbackQueryHandler(callback=delete_product_hand, pattern="delete_product")
