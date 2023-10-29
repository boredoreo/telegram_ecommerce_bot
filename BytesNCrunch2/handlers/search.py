import logging, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackQueryHandler, CommandHandler,  Filters, Updater, ConversationHandler, MessageHandler
from telegram.files.inputmedia import InputMediaPhoto
from database.models import  Vendor, Student, Product
from database.manipulate import load_blob
from database.query import get_all_vendors, get_my_products


def search(update,bot):
    bot.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Feature Coming Soon"
    )

search_handler = CommandHandler("search", search)