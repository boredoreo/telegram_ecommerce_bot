import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler
import os
from dotenv.main import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
NAME, MATRIC_NO, HALL, DESCRIPTION, EMAIL, SUMMARY, CHECK, NAME_MESSAGE= range(8)
complaint = {
    'username': 'null',
    'full_name': '',
    'matric_no': '',
    'hall_roomno': '',
    'description': '',
    'email': '',
    'category': ','
}
def add_complaint(update: Update, bot):
    
    reply_keyboard = [
        [InlineKeyboardButton(text="Payment Complaint", callback_data="PAYMENT COMPLAINT")],
        [InlineKeyboardButton(text="Delivery Complaint", callback_data="DELIVERY COMPLAINT")],
        [InlineKeyboardButton(text="Others", callback_data="OTHER COMPLAINT")]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    update.message.reply_text(
        text="Please select your complaint category: ", reply_markup=markup
    )
    user = update.message.from_user
    username = user.username
    if username:
        complaint['username'] = user.username
        return NAME
    return NAME
    
def name(update, context):
    query = update.callback_query
    logger.info("THis user chose %s", query.data)
    complaint['category'] = query.data
    query.answer()
    query.edit_message_text("Please input your full-name: ")

    return MATRIC_NO
 
def name_message(update, context):
    user_message = update.message.text
    logger.info("This user chose %s'", user_message)
    update.message.reply_text("Please input your full-name: ")
    return MATRIC_NO

def matric_no(update, context):
     query = update.callback_query
     logger.info("THis user's fullname is %s'", update.message.text)
     complaint["full_name"] = update.message.text
     update.message.reply_text("Please input Matric number: ")
     
     return HALL
 
def hall(update, context):
     query = update.callback_query
     logger.info("THis user's matric number is %s'", update.message.text)
     complaint["matric_no"] = update.message.text
     update.message.reply_text("Please enter you hall and room number eg: Daniel E403: ")
     
     return EMAIL
 
def email(update, context):
     query = update.callback_query
     logger.info("THis user's room number is %s'", update.message.text)
     complaint["hall_roomno"] = update.message.text
     update.message.reply_text("Please input Email address: ")
     
     return DESCRIPTION
 
def desc(update, context):
     query = update.callback_query
     logger.info("This user's email is %s'", update.message.text)
     complaint["email"] = update.message.text
     update.message.reply_text("Please input your complaint description: ")
     
     return SUMMARY
 
def summary(update, context):
     query = update.callback_query
     logger.info("THis user's complaint is %s'", update.message.text)
     complaint["description"] = update.message.text
     reply_keyboard = [
        [InlineKeyboardButton(text="YES", callback_data="YES")],
        [InlineKeyboardButton(text="NO", callback_data="NO")]
     ]
     print(complaint['description'])
     markup = InlineKeyboardMarkup(reply_keyboard)
     update.message.reply_text(text="""Here are your details:\n "Category":{} \n Name: {} \n Matric number: {} \n Room_number: {} \n Complaint: {} \n\n are these details correct?
                               
                               """.format(complaint['category'], complaint["full_name"],
                                          complaint["matric_no"], complaint["hall_roomno"],
                                          complaint["description"]), reply_markup=markup)
     return CHECK
 
def check(update, context):
    query = update.callback_query
    logger.info("This user's check is %s'", query.data)
    check = query.data

    if check == 'YES':
        query.answer()
        query.edit_message_text("Thank you for your feedback, we'll get back to you shortly\n")
        group_chat_id = os.getenv('group_id')
        summary_text = f"Category: {complaint['category']}\nName: {complaint['full_name']}\nMatric number: {complaint['matric_no']}\nRoom_number: {complaint['hall_roomno']}\nComplaint: {complaint['description']}"
        context.bot.send_message(chat_id=group_chat_id, text=summary_text)
        return ConversationHandler.END
    elif check == 'NO':
        query.answer()
        query.edit_message_text("please input 'continue'\n")
        return NAME_MESSAGE
    
        
    

def cancel(update, context) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END   

complaint_handler = ConversationHandler(
    entry_points = [CommandHandler('complaint',add_complaint)],
    states={
        NAME: [CallbackQueryHandler(name)],
        NAME_MESSAGE: [MessageHandler(Filters.text & ~Filters.command, name_message)],
        MATRIC_NO: [MessageHandler(Filters.text & ~Filters.command, matric_no)],
        HALL: [MessageHandler(Filters.text & ~Filters.command, hall)],
        DESCRIPTION: [MessageHandler(Filters.text & ~Filters.command, desc)],
        EMAIL: [MessageHandler(Filters.text & ~Filters.command, email)],
        SUMMARY: [MessageHandler(Filters.text & ~Filters.command, summary)],
        CHECK: [CallbackQueryHandler(check)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    )
