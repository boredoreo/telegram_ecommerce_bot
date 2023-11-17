from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackQueryHandler
from database.query import get_product
from filters.helpers import compute_rates





def checkout(update, bot):
    query = update.callback_query
    data = update.callback_query.data
    total = int(bot.user_data["cart_total"])
    rate = compute_rates(total)
    reply_keyboard = [
        [
            InlineKeyboardButton(text="Bank tranfer to Byte n Crunch", callback_data="direct_transfer")
        ] ,
        [
            InlineKeyboardButton(text="Pay with FLutterwave", callback_data="pay_with_flutter_wave")
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text=f"You total comes down to # {total+rate} \n Subtotal: #{total} \n Shipping : #{rate}",
        reply_markup=markup,
    )


check_out_handler = CallbackQueryHandler(callback=checkout, pattern="checkout")