from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/bonus', methods=['POST'])
def add_bonus():
    data = request.json
    user_id = data.get('user')
    bonus = 0.92*float(data.get('bonus')) # 92%

    if user_id and bonus:
        #Simulação de bonus
        #TODO: poderia usar uma cache para guardar os bonus??
        return jsonify({
            'status': 'success',
            'message': 'Bonus of {} = {}'.format(user_id, bonus),
            'bonus': bonus
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid request'
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)