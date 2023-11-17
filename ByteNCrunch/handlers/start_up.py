from database.models import User, Student
from database.query import (
    get_user,
    is_user,
)

from database.manipulate import (
    commit_user,
    commmit_student
)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    ConversationHandler,
    MessageHandler,
)


# start handler
def start(update, bot):
    exist = is_user(update.effective_user.id) 
    if exist:
        user_type = get_user(update.effective_user.id)
        role = user_type.role
        reply_keyboard = [
            [InlineKeyboardButton(text="Customer Support", callback_data="customer_feedback")],
            [InlineKeyboardButton(text="Make Order", callback_data="make_order")]
        ]
        markup = InlineKeyboardMarkup(reply_keyboard)
        bot.bot.send_message(
            chat_id=update.effective_chat.id,
            text="""
                Welcome to Byte & Crunch! \n How may we be of assistance to you?
                ***SUBJECT TO CHANGE***
                """,
            reply_markup=markup
        )
        
    else:
        reply_keyboard = [
            [InlineKeyboardButton(text="Let's Go!", callback_data="is_customer")],
        ]
        bot.user_data["user"] = User()
        markup = InlineKeyboardMarkup(reply_keyboard)
        bot.bot.send_message(
            chat_id=update.message.chat_id,
            text="Welcome to Byte & Crunch Telegram Bot!",
            reply_markup=markup,
        )

        return 0


#is customer
def setup_customer(update, bot):
    query = update.callback_query
    user = bot.user_data["user"]
    user.userid = update.effective_user.id
    user.role = "customer"
    "userid VARCHAR(120) UNIQUE, name VARCHAR(120), matno CHAR(10) UNIQUE, regno CHAR(7) UNIQUE, room VARCHAR(255)"
    query.edit_message_text(
            text="""
                Thank you for chooosing Byte & Crunch!
                \nWe need some information before you can continue to ordering your food!
                \nPlease reply with your:
                \n<name>, <matric number>, and <hall and room number>
                \nIn that order separated by full stops
                \neg
                \nOreo Eniola.19Ck000000.Daniel Hall F208 
                """
            )
    bot.user_data["user"] = user
    bot.user_data["role"] = user.role
    # result = update.message.text.split(".")
    # print(result)
    print("done")

    return "c_0"


def customer_detail(update, bot):
    user_id = update.effective_user.id
    role = bot.user_data["role"]
    result = update.message.text.split(".")
    print(result)
    name, matno, room = result
    
    bot.user_data["user_type"] = Student(
        role=role, userid=user_id, name=name, matno=matno, room=room
    )

    reply_keyboard = [
        [InlineKeyboardButton(text="Yes, Submit!", callback_data="save")],
        [InlineKeyboardButton(text="No, Re-enter Details", callback_data="return")],
    ]
    mark_up = InlineKeyboardMarkup(reply_keyboard)
    bot.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""
            Here's what you entered: \n
            Name =>{name}
            Matric No => {matno}
            Room details => {room}

            Is this all correct?

            """,
        reply_markup=mark_up,
    )
    return "submit"



# save user to database
def submit(update, bot):
    chat_id = update.effective_chat.id
    bot.user_data["cart"] = {}
    bot.user_data["cart_total"] = 0
    current_user = bot.user_data["user"]
    user_type = bot.user_data['user_type']
    role = bot.user_data["role"]
    if update.callback_query.data == "save":
        commit_user(current_user)
        commmit_student(user_type)        
        bot.bot.send_message(
            text="Account Created Successfully! \n /start to view your commands ",
            chat_id=update.effective_chat.id,
        )

        del bot.user_data["role"]
        del bot.user_data['user_type']
        del bot.user_data["user"]
        return ConversationHandler.END

        
    elif update.callback_query.data == "return":
        bot.bot.send_message(
            chat_id=update.effective_chat.id,
               text="""
                    Please reply with your:
                    \n<name>, <matric number>, and <hall and room number>
                    \nIn that order separated by full stops
                    \neg
                    \n\nOreo Eniola.19Ck000000.Daniel Hall F208 
                    """,
                )
        return "c_0"

    return ConversationHandler.END

def cancel(update,bot):
	update.message.reply_text('Operation canceled')
	return ConversationHandler.END


start_handler = CommandHandler("start", start, run_async=True)
setup_user_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(pattern="is_customer", callback=setup_customer, run_async=True)
        ],
    states= {
        "c_0" : [MessageHandler(Filters.all, customer_detail, run_async=True)],
        "submit": [CallbackQueryHandler(submit, run_async=True)]

    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
back_to_home = CallbackQueryHandler(callback=start, pattern="start")
