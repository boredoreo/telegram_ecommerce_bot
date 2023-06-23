# Handlers for initial account creation

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackQueryHandler, CommandHandler,  Filters, Updater, ConversationHandler, MessageHandler
from new_models import User, Vendor, Student

# user instance
current_user = User()

# start handler
def start( update, bot):
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
        else:
            reply_keyboard = [
                [InlineKeyboardButton(text="Let's Go!", callback_data="go")],
            ]
            markup = InlineKeyboardMarkup(reply_keyboard)
            bot.bot.send_message(
                chat_id = update.message.chat_id,
                text = "Welcome to Byte & Crunch Telegram Bot!",
                reply_markup = markup

            )
            
            return 0
# choose user type
def choose( update, bot):
    query = update.callback_query
    reply_keyboard = [
        [InlineKeyboardButton(text="Vendor", callback_data="vendor")],
        [InlineKeyboardButton(text="Customer", callback_data="customer")],
        [InlineKeyboardButton(text="Delivery Agent", callback_data="dispatcher")]
    ]
    mark_up = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text = "How do you plan on using this bot?",
        reply_markup = mark_up
    )
    return 1

# handle account creation based on chosen roles
def sort_roles( update, bot):
    query = update.callback_query
    role = update.callback_query.data
    chat_id = update.effective_chat.id
    current_user.userid, current_user.role = update.effective_user.id, role
    current_user.role = role
       
    match role:
        case "vendor":
            # current_user.user_type = Vendor(userid=current_user.userid, name=)
            query.edit_message_text(
                text = '''
                Welcome Aboard! \nCould you please tell me about your business? \nPlease reply with your: \n<Name>, <Business Name>, <email> and <Phone Number>
                \nIn that order separated by commas
                \neg
               \n Uche, Bolt, bolt@gmail.com ,09000000000 
                '''
            )
            return "vendor"
        case "customer":
            "userid VARCHAR(120) UNIQUE, name VARCHAR(120), matno CHAR(10) UNIQUE, regno CHAR(7) UNIQUE, room VARCHAR(255)"
            query.edit_message_text(
                text = '''
                Thank you for chooosing Byte & Crunch!
                \nWe need some information before you can continue to ordering your food!
                \nPlease reply with your:
                \n<name>, <matric number>, and <hall and room number>
                \nIn that order separated by full stops
                \neg
                \nOreo Eniola.19Ck000000.Daniel Hall F208 
                '''
            )
            return "student"

        case "dispatcher":
            "userid VARCHAR(120) UNIQUE, name VARCHAR(120), matno CHAR(10) UNIQUE, regno CHAR(7) UNIQUE, room VARCHAR(255)"
            query.edit_message_text(
                text = '''
                Thank you for Partnering with Byte & Crunch!
                \nWe need some information before you can continue to making your first delivery!
                \nPlease reply with your:
                \n<name>, <matric number>, and <hall and room number>
                \nIn that order separated by full stops
                \neg
                \n\nOreo Eniola.19Ck000000.Daniel Hall F208 
                '''
            )
            return "student"
# receive and confirm entered details for vendors
def vendor_detail( update, bot):
        user_id = update.effective_user.id
        role = current_user.role
        result = (update.message.text).split(",")
        name, shop_name,email, phone_no = result
        current_user.user_type=Vendor(userid=user_id,name=name,shop_name=shop_name,email=email,phone_no=phone_no)
        reply_keyboard = [
            [InlineKeyboardButton(text="Yes, Submit!", callback_data="save")],
            [InlineKeyboardButton(text="No, Re-enter Details", callback_data="return")]
        ]
        mark_up = InlineKeyboardMarkup(reply_keyboard)
        bot.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'''
            Here's what you entered: \n
            Name =>{name}
            Business Name => {shop_name}
            Phone Number => {phone_no}
            Email => {email}


            Is this all correct?

            ''',
            reply_markup=mark_up
        )

        return 2

# receive and confirm entered details for vendors
def student_detail( update, bot):
        user_id = update.effective_user.id
        role = current_user.role
        result = (update.message.text).split(".")
        name, matno, room = result
        print(result)
        print(role)
        current_user.userid =user_id
        current_user.role = role
        current_user.user_type = Student(role=role, userid=user_id, name=name, matno=matno, room= room,)
        reply_keyboard = [
            [InlineKeyboardButton(text="Yes, Submit!", callback_data="save")],
            [InlineKeyboardButton(text="No, Re-enter Details", callback_data="return")]
        ]
        mark_up = InlineKeyboardMarkup(reply_keyboard)
        bot.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'''
            Here's what you entered: \n
            Name =>{name}
            Matric No => {matno}
            Room details => {room}

            Is this all correct?

            ''',
            reply_markup=mark_up
        )
        return 2
# save user to database
def submit( update, bot):
        chat_id = update.effective_chat.id
        if update.callback_query.data == "save":
            try:
                current_user.commit()
            except:
                current_user.user_type.commit()
            bot.bot.send_message(
                text = "Account Created Successfully! \n /start to view your commands ",
                chat_id = update.effective_chat.id
            )
        elif update.callback_query.data == "return":
            role = current_user.role
            match role:
                case "dispater" | "customer":
                    bot.bot.send_message(
                            chat_id = update.effective_chat.id,
                            text = '''
                            Please reply with your:
                            \n<name>, <matric number>, and <hall and room number>
                            \nIn that order separated by full stops
                            \neg
                            \n\nOreo Eniola.19Ck000000.Daniel Hall F208 
                            '''
                        )
                    return "student"

                case "vendor":
                    bot.bot.send_message(
                            chat_id = update.effective_chat.id,
                            text = '''
                             \nPlease reply with your: \n<Name>, <Business Name>, <email> and <Phone Number>
                    \nIn that order separated by commas
                    \neg
                   \n Uche, Bolt, bolt@gmail.com ,09000000000 
                            '''
                        )
                    return "vendor"
