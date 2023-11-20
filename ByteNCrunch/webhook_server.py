from flask import Flask, request, make_response, jsonify
import os
import json

app = Flask(__name__)

@app.route('/flutterwave_webhook', methods=['POST'])
def flutterwave_webhook():
    data = request.get_json()
    secret_hash = os.getenv("FLW_SECRET_HASH")
    signature = request.headers.get("verifi-hash")

    if signature is None or (signature != secret_hash):
        return make_response("Unauthorized", 401)

    payload = request.get_data(as_text=True)
    response = make_response("OK", 200)

    data = json.loads(payload)
    email = data["customer"]["email"]
    status = data["status"]
    reference = data["txRef"]

   

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
