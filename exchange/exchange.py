from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/exchange', methods=['GET'])
def get_exchange_rate():
    # Gera uma taxa aleatória para simular um valor real
    exchange_rate = random.randint(4, 10)
    return jsonify({'exchange_rate': exchange_rate}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
