# import logging, os
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
# from telegram.ext import  CallbackQueryHandler, CommandHandler,  Filters, Updater, ConversationHandler, MessageHandler
# from telegram.files.inputmedia import InputMediaPhoto
# from database.models import User, Vendor, Student, Product
# from database.manipulate import load_blob
# from database.query import get_all_vendors

# def edit_product(update, bot):
#     query = update.callback_query
#     product_id = query.data[13:]
#     current_product=Product()
#     current_product.instance=product_id


#     bot.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text='''
#         Enter the name of your product name, and price separated by a  comma
#         eg 
#         <Potato,1000>
#         \n**Don't add a hashtag(#) or an 'N' to indicate currency, numbers only
#         '''
#     )
#     return 0

# def edit_product_finish(update,bot):
#     query = update.callback_query
#     product_id = query.data[13:]
#     current_product=Product()
#     current_product.instance=product_id
#     file_name = "{}.jpg".format(current_product.name)
#     file = bot.bot.get_file(update.message.photo[-1].file_id)
#     file.download(file_name)
#     print(current_product.name, current_product.description, current_product.price, current_product.instance)
    
#     print(current_product.name)
#     if os.path.exists(file_name):
#         with open(file_name, 'rb') as f:
#             current_product.image = f.read()
#         current_product.edit(current_product.name,current_product.image, current_product.description, current_product.price, current_product.instance)
#         os.remove(file_name)

#     return


# def delete_product(update,bot):
#     query =  update.callback_query
#     product_id = query.data[15:]
#     print(product_id) 


# edit_product_handler = ConversationHandler(
#     entry_points=[CallbackQueryHandler(pattern="edit_product_", callback=edit_product,run_async=True)],
#     states={
#         0:[MessageHandler(Filters.all, add_product_description)],
#         1:[MessageHandler(Filters.all, add_product_picture)],
#         2:[MessageHandler(Filters.all, edit_product_finish)]            
#     },
#     fallbacks=[]
# )

# delete_product_handler = CallbackQueryHandler(callback=delete_product, pattern="delete_product")
