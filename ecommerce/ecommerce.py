from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


def seek_product(product_id):
    # Request para Store, via get
    response = requests.get('http://<ip_store>:5001/product', params={"product": product_id})

    #Verificação se o produto foi encontrado
    if response.status_code == 200: #OK
        return response.json()
    else:
        return None

@app.route('/buy', methods=['GET'])
def buy():
    product_id = request.args.get("product_id")
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