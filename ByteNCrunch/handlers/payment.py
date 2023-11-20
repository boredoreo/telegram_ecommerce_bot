from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackQueryHandler
from filters.helpers import compute_rates
from database.models import FlutterPayment
import uuid
import requests
import os
from dotenv.main import load_dotenv
from database.query import get_product

load_dotenv()

def flutterwave_handler(update, bot):
    my_order = ""
    cart = list(bot.user_data["cart"].items())
    query = update.callback_query
    total = int(bot.user_data["cart_total"])
    data = update.callback_query.data
    rate = compute_rates(total)
    subtotal = total + rate
    for i in cart:
        product = get_product(i[0])
        my_order += "{} orders of {} at {} paid {}".format(i[1], product[1], (int(product[3]) *i[1]), subtotal)
    
    print(subtotal)
    print("space")
    print(my_order)
    reference = str(uuid.uuid4())
    payment = FlutterPayment(amount=subtotal, reference=reference, user_id=update.effective_user.id, order_item=my_order)
    payment.save()
    
    
    
def initialize_payment(self, reference, amount, email, currency):
        flutterwave_url = 'https://api.flutterwave.com/v3/payments'
        
        secret_key = os.environ["FLUTTERWAVE_SECRET_KEY"]
        headers = {
            'Authorization': f'Bearer {secret_key}',
            'Content-Type': 'application/json',
        }
        # amount = amount * 100
        data = {
            'tx_ref': reference,
            'amount': amount,
            'currency': currency,
            'customer': {
                'email': email
            },
            'customizations': {
                'title': "BytenCrunch"
            },
            'redirect_url': 'http://127.0.0.1:5000/flutterwave_webhook'
        }
        
        response = requests.post(flutterwave_url, headers=headers, json=data)
        return response.json()
    







flutterwave_payment_handler = CallbackQueryHandler(callback=flutterwave_handler, pattern="pay_with_flutter_wave")