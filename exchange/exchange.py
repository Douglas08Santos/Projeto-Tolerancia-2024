from flask import Flask, jsonify
import requests
import os

EXCHANGE_RATE_API_KEY = '07509480328ffa2422cd1b75'
EXCHANCE_RATE_API_URL = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD'
SERVICE_NAME = os.environ.get('SERVICE_NAME', 'unknown')

app = Flask(__name__)

@app.route('/exchange', methods=['GET'])
def get_exchange_rate():
    response = requests.get(EXCHANCE_RATE_API_URL)
    data = response.json()
    exchange_rate = data['conversion_rates']['BRL']
    return jsonify(
        {'exchange_rate': exchange_rate, 'service': SERVICE_NAME}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
