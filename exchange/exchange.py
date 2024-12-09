from flask import Flask, jsonify
import random
import requests

EXCHANGE_RATE_API_KEY = '07509480328ffa2422cd1b75'
EXCHANCE_RATE_API_URL = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD'

app = Flask(__name__)

@app.route('/exchange', methods=['GET'])
def get_exchange_rate():
    response = requests.get(EXCHANCE_RATE_API_URL)
    data = response.json()
    exchange_rate = data['conversion_rates']['BRL']
    return jsonify({'exchange_rate': exchange_rate}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
