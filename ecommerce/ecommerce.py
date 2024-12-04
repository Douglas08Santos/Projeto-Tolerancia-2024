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

@app.route('/buy', methods=['GET'])
def buy():
    product_id = request.args.get("product")
    print(product_id)
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
        return jsonify({
            "status": "success",
            "product":product_data
        }), 200
    else:
        return jsonify({
            "status":"error",
            "message": "Product not found"
        }), 404

if __name__== '__main__':
    app.run(host='0.0.0.0', port=5000)