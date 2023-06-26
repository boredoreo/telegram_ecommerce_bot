from database.models import User

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler,CallbackQueryHandler

def start(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "hey"
    )
    return 0

def rec(update, context):
    data = update.message.text
    user = User(userid=update.effective_user.id, role=data)
    context.user_data["user"] = user

    reply_keyboard = [
        [InlineKeyboardButton(text="Vendor", callback_data="vendor")],
        [InlineKeyboardButton(text="Customer", callback_data="customer")],
        [InlineKeyboardButton(text="Delivery Agent", callback_data="dispatcher")]
    ]
    mark_up = InlineKeyboardMarkup(reply_keyboard)
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "done",
        reply_markup = mark_up
    )
    return 1

def vec(update, context):
    user =  context.user_data["user"]
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "{}\n{}".format(user.userid,user.role)
    )
    del context.user_data["user"]

    return ConversationHandler.END

def fin(update, context):
    user =  context.user_data["user"]
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "ex{}\n{}".format(user.userid,user.role)
    )

updater =Updater("5920244560:AAFNJlpyon0kr-AO7nQqi9cleIxvBak7BmA")
dispatcher = updater.dispatcher

start_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)], 
    states = {
        0: [MessageHandler(Filters.all, rec)],
        1:[CallbackQueryHandler(vec)],

    }, fallbacks = [])
dispatcher.add_handler(start_handler)

test_hand = CommandHandler("test", fin)
dispatcher.add_handler(test_hand)

updater.start_polling()
