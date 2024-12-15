import random
import time
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# Exemplos de produtos do estoque
products = {
    1:{'id':1, 'name':'Product A', 'value': 100.0, 'stock': 10}, # Value USD
    2:{'id':2, 'name':'Product B', 'value': 200.0, 'stock': 10},
    3:{'id':3, 'name':'Product C', 'value': 300.0, 'stock': 10}  
}

@app.route('/product', methods=['GET'])
def get_product():
    # Simular falha de 'Omission', com taxa de 20%
    if random.random() < 0.2:
        return jsonify({'message':'Omission'}), 404
    
    # Captura do parâmetros enviado pelo request'Product not found'
    product_id = request.args.get('product')

    #Validação ser o id é valido e se existe na lista de produtos
    if product_id and int(product_id) in products:
        product = products[int(product_id)]
        return jsonify(product), 200
    else:
        return jsonify({'status': 'error', 'message':'Product not found'}), 404
    
@app.route('/sell', methods=['POST'])
def sell():
    # Simular falha de 'Error', com taxa de 10%, durante 5s
    if random.random() < 0.1:
        time.sleep(5)
        return jsonify({'message':'Error'}), 404
    
    data = request.json
    product_id = data.get('product')

     # Verificação se ainda tem o produto em estoque
    if products[int(product_id)]['stock'] > 0:     
        #Gera um id para a transação de compra
        transaction_id = str(uuid.uuid4())
        products[int(product_id)]['stock'] -= 1
        return jsonify({'transaction_id': transaction_id}), 200
    else:
        '''
            409 Conflict
            Situações em que a requisição do cliente não pode ser
            concluída devido a um conflito com o estado atual do 
            recurso no servidor
        '''
        return jsonify({'status': 'error', 'message':'Product out of stock'}), 409


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)