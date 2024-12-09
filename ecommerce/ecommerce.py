from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

latest_usd_exchange_rate = 1.0

def seek_product(product_id):
    # Request para Store, via get
    response = requests.get('http://store:5001/product', params={'product': product_id})

    #Verificação se o produto foi encontrado
    if response.status_code == 200: #OK
        return response.json()
    else:
        return None
    
def get_exchange():
    try:
        response = requests.get('http://exchange:5002/exchange') # colocar num try-catch
        global latest_usd_exchange_rate

        if response.status_code == 200:
            data = response.json()
            latest_usd_exchange_rate = data['exchange_rate']
            return latest_usd_exchange_rate
        else:
            return latest_usd_exchange_rate
        # implementar um catch para tratar a exceção (log)
    finally:
            return latest_usd_exchange_rate

def make_purchase(product_id):
    response = requests.post('http://store:5001/sell', json={'product': product_id})

    if response.status_code == 200:
        return response.json()['transaction_id']
    else: 
        return None
    
def send_bonus(user_id, bonus):
    response = requests.post('http://fidelity:5003/bonus', json={"user": user_id, "bonus":bonus})
    if response.status_code == 200:
        return response.json()['bonus']
    else: 
        return None


@app.route('/buy', methods=['POST'])
def buy():
    data = request.json
    product_id = data.get("product")
    user_id = data.get("user")
    
    print(product_id, user_id)
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
                A resposta deve ser um número real positivo que indica a taxa
                de conversão da moeda.       
        '''
        exchange_rate = get_exchange()
        product_exchange_value = round(product_data['value']*exchange_rate, 2) # Converte para BRL
        
        '''
            Request 3:
                O E-commerce envia um request para o Store, via POST para o
                endpoint /sell, com os seguintes parâmetros:
                    - product – id do produto a ser comprado
                A resposta deve conter um id único da transação (gerado automaticamente) que
                representa essa venda.
        '''
        transaction_id = make_purchase(product_id)

        '''
            Request 4:
                O E-commerce envia um request para o Fidelity, via POST para o endpoint /bonus, com os seguintes parâmetros:
                    - user – id do usuário que está executando a compra
                    - bonus – um valor inteiro mais próximo do valor do
                    produto antes da conversão
                A resposta deve indicar o sucesso da operação (HTTP Responde Code).
        '''
        bonus = send_bonus(user_id, product_data['value'])
        
        return jsonify({
            'status': 'success',
            'product':product_data,
            'exchange_rate': exchange_rate,
            'exchange_value': product_exchange_value,
            'transaction_id': transaction_id,
            'bonus': bonus
        }), 200
    else:
        return jsonify({
            'status':'error',
            'message': 'Product not found'
        }), 404

if __name__== '__main__':
    app.run(host='0.0.0.0', port=5050)