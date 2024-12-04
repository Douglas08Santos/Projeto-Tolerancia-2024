from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


def seek_product(product_id):
    # Request para Store, via get
    response = requests.get('http://localhost:5001/product', params={"product": product_id})

    #Verificação se o produto foi encontrado
    if response.status_code == 200: #OK
        return response.json()
    else:
        return None
    

def get_exchange():
    response = requests.get('http://localhost:5003/exchange')

    return response.json()['exchange_rate']

@app.route('/buy', methods=['GET'])
def buy():
    product_id = request.args.get("product")
    
    
    '''
        Requisição nº1 - Product
            O E-commerce envia um request para o Store, via GET para o
            endpoint /product, com os seguintes parâmetros:
                - product: id do produto a ser comprado
            A resposta deve ser um json com os dados do produto consultado e
            deve ter as seguintes informações: id, name, value
    '''
    product_data = seek_product(product_id)

    if product_data:
        #Calcular o preço convertido
        '''
            Request 2:
                O E-commerce envia um request para o Exchange, via GET para o
                endpoint /exchange, sem parâmetros. 
                A resposta deve ser um número real positivo que indica a taxa de conversão da moeda.       
        '''
        exchange_rate = get_exchange()
        product_exchange_value = round(product_data['value']/exchange_rate, 2)
        
        return jsonify({
            "status": "success",
            "product":product_data,
            "exchange_rate": exchange_rate,
            "exchange_value": product_exchange_value
        }), 200
    else:
        return jsonify({
            "status":"error",
            "message": "Product not found"
        }), 404

if __name__== '__main__':
    app.run(host='0.0.0.0', port=5000)