import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackQueryHandler, CommandHandler,  Filters, Updater, ConversationHandler, MessageHandler
from new_models import User, Vendor, Student

current_user= User()
def greet(update,bot):
        current_user = User()
        if current_user.is_user(update.effective_user.id):
            current_user  = User(instance=update.effective_user.id)
            role = current_user.role
            match role:
                case "vendor":
                    bot.bot.send_message(
                        chat_id = update.effective_chat.id,
                        text = '''
                        Thanks for partnering with us!\nHere's a list of commands available to you:
                        /add_product
                        /view_products
                        '''
                    )
                    return 
                case "customer":
                    bot.bot.send_message(
                        chat_id = update.effective_chat.id,
                        text = '''
                        Thanks for partnering with us!\nHere's a list of commands available to you:
                        /add_product
                        /view_products
                        '''
                    )
                    return
                case "dispatcher" :
                    bot.bot.send_message(
                        chat_id = update.effective_chat.id,
                        text = '''
                        Thanks for partnering with us!\nHere's a list of commands available to you:
                        /add_product
                        /view_products
                        '''
                    )
                    return 
            return 