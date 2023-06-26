import logging, os
from handlers import all_handlers
from config import TOKEN
from telegram.ext import Updater 




if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    for handler in all_handlers:
        dispatcher.add_handler(handler)


    updater.start_polling()