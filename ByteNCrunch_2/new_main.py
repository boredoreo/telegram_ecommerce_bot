import logging, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackQueryHandler,Handler, CommandHandler,  Filters, Updater, ConversationHandler, MessageHandler
from new_models import User, Vendor, Student

from dotenv.main import load_dotenv

load_dotenv()



if __name__ == "__main__":
    from start_up_handlers import *
    from general_handlers import *
    from vendor_handlers import *
    from customer_handlers import *


    token = os.environ["TOKEN"]
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    settings = ""
    updater = Updater(token)
    dispatcher = updater.dispatcher
    start_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start,run_async=True)],
        states = {
            0: [CallbackQueryHandler( choose,run_async=True)],
            1: [CallbackQueryHandler(sort_roles,run_async=True)],
            "vendor":[MessageHandler(Filters.all,vendor_detail, run_async=True)],
            "student":[MessageHandler(Filters.all,student_detail, run_async=True)],
            2:[CallbackQueryHandler(submit,run_async=True)],
            3:[MessageHandler(Filters.all,greet,run_async=True)],
            "greet":[CallbackQueryHandler(greet,run_async=True)]

        },
        fallbacks=[CommandHandler("start", start,run_async=True)]
        )

    add_product_handler = ConversationHandler(
        entry_points=[CommandHandler("add_product", add_product,run_async=True)],
        states={
            0:[MessageHandler(Filters.all, add_product_description,run_async=True)],
            1:[MessageHandler(Filters.all, add_product_picture,run_async=True)],
            2:[MessageHandler(Filters.all, add_product_finish, )],
            
            
        },
        fallbacks=[CommandHandler("add_product", add_product,run_async=True)])
    greet_handler = CommandHandler("hello", greet,run_async=True)

    products_handler = CommandHandler("view_products", view_products)

    view_products_handler = CallbackQueryHandler(pattern="view_product_", callback=view_products_extended)
    edit_product_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(pattern="edit_product_", callback=edit_product,run_async=True)],
        states={
            0:[MessageHandler(Filters.all, add_product_description)],
            1:[MessageHandler(Filters.all, add_product_picture)],
            2:[MessageHandler(Filters.all, edit_product_finish)]
            
        },
        fallbacks=[]
        )

    browse_vendor_handler = CommandHandler("browse_stores", browse_vendors,run_async=True)
    browse_vendor_ext_handler = CallbackQueryHandler(callback=browse_vendors_extended, pattern="browse_vendor_", run_async=True)

    


    dispatcher.add_handler(browse_vendor_handler)
    dispatcher.add_handler(browse_vendor_ext_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(greet_handler)
    dispatcher.add_handler(add_product_handler)
    dispatcher.add_handler(products_handler)
    dispatcher.add_handler(view_products_handler)
    dispatcher.add_handler(edit_product_handler)
    updater.start_polling()