from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# Exemplos de produtos do estoque
products = {
    1:{'id':1, 'name':'Product A', 'value': 100.0}, # Value USD
    2:{'id':2, 'name':'Product B', 'value': 200.0}, # checar estoque (atributo quantidade)
    3:{'id':3, 'name':'Product C', 'value': 300.0}  
}

@app.route('/product', methods=['GET'])
def get_product():
    # Captura do parâmetros enviado pelo request
    product_id = request.args.get('product')


    #Validação ser o id é valido e se existe no estoque
    if product_id and int(product_id) in products:
        product = products[int(product_id)]
        print(product)
        return jsonify(product), 200
    else:
        return jsonify({'status': 'error', 'message':'Product not found'}), 404
    
@app.route('/sell', methods=['POST'])
def sell():
    data = request.json
    product_id = data.get('product')

    # Verificação ser o product_id não é nulo e se ele existe
    # TODO: Será que precisa verificar 2 vezes??
    if product_id and int(product_id) in products:
        #Gera um id para a transação de compra
        transaction_id = str(uuid.uuid4())
        return jsonify({'transaction_id': transaction_id})
    else:
        return jsonify({'status': 'error', 'message': 'Product not found'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)