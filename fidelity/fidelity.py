import random
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

server_bonus = {}

@app.route('/bonus', methods=['POST'])
def add_bonus():
    # Simular falha de 'Timeout', com taxa de 10%, durante 30s
    if random.random() < 0.1:
        time.sleep(30)
        return jsonify({'message':'Timeout'}), 408
    
    
    data = request.json
    user_id = data.get('user')
    bonus = 0.92*float(data.get('bonus')) # 92%

    if user_id and bonus:
        #Simulação de bonus
        if user_id in server_bonus.keys():
            server_bonus[user_id] += bonus
        else:
            server_bonus[user_id] = 0
            server_bonus[user_id] += bonus
        
        return jsonify({
            'status': 'success',
            'message': 'Bonus of {} = {}'.format(user_id, bonus),
            'bonus': bonus,
            'amount_bonus': server_bonus[user_id]
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid request'
        }), 400
    
@app.route('/show', methods=['GET'])
def show_bonus():
    return jsonify(server_bonus)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)