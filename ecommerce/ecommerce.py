from itertools import product
from math import prod
from flask import Flask, request, jsonify

from ft import ft_get_exchange, ft_make_purchase, ft_seek_product, ft_send_bonus
from noft import noft_get_exchange, noft_make_purchase, noft_seek_product, noft_send_bonus


app = Flask(__name__)

@app.route('/buy', methods=['POST'])
def buy():
    data = request.json
    product_id = data.get("product")
    user_id = data.get("user")
    ft = data.get("ft")

    # ft = 0 - Fault Tolerante is OFF
    # ft != 0 - Fault Tolerance is ON
    if ft != 0:
        '''
            Requisição nº1 - Product
                O E-commerce envia um request para o Store, via GET para o
                endpoint /product, com os seguintes parâmetros:
                    - product: id do produto a ser comprado
                A resposta deve ser um json com os dados do produto consultado e
                deve ter as seguintes informações: id, name, value
        '''
        seek_product = ft_seek_product(product_id)
        if seek_product['status_code'] == 200:
            product_data = seek_product['product']
        else:
            return jsonify({
                'status':'error',
                'message': seek_product['message']
            }), seek_product['status_code'] 

       
        #Calcular o preço convertido
        '''
            Request 2:
                O E-commerce envia um request para o Exchange, via GET para o
                endpoint /exchange, sem parâmetros. 
                A resposta deve ser um número real positivo que indica a taxa
                de conversão da moeda.       
        '''
        exchange_rate = ft_get_exchange()
        product_exchange_value = round(float(product_data['value'])*exchange_rate, 2) # Converte para BRL
        '''
            Request 3:
                O E-commerce envia um request para o Store, via POST para o
                endpoint /sell, com os seguintes parâmetros:
                    - product – id do produto a ser comprado
                A resposta deve conter um id único da transação (gerado automaticamente) que
                representa essa venda.
        '''
        make_purchase = ft_make_purchase(product_id)
        if make_purchase['status_code'] == 200:
            transaction_id = make_purchase['transaction_id']
        else:
            return jsonify({
                'status':'error',
                'message': make_purchase['message']
            }), make_purchase['status_code']

        '''
            Request 4:
                O E-commerce envia um request para o Fidelity, via POST para o endpoint /bonus, com os seguintes parâmetros:
                    - user – id do usuário que está executando a compra
                    - bonus – um valor inteiro mais próximo do valor do
                    produto antes da conversão
                A resposta deve indicar o sucesso da operação (HTTP Responde Code).
        '''
        send_bonus = ft_send_bonus(user_id, product_data['value'])
        if send_bonus['status_code'] == 200:
            bonus = send_bonus['bonus']
        else:
            return jsonify({
                'status':'error',
                'message': send_bonus['message']
            }), send_bonus['status_code']

        return jsonify({
            'status': 'success',
            'product':product_data,
            'exchange_rate': exchange_rate,
            'exchange_value': product_exchange_value,
            'transaction_id': transaction_id,
            'bonus': bonus
        }), 200
    else:
        # No Fault Tolerance
        product_data = noft_seek_product(product_id)
        exchange_rate = noft_get_exchange()
        product_exchange_value = round(product_data['value']*exchange_rate, 2) # Converte para BRL
        transaction_id = noft_make_purchase(product_id)
        bonus = noft_send_bonus(user_id, product_data['value'])
        return jsonify({
                'status': 'success',
                'product':product_data,
                'exchange_rate': exchange_rate,
                'exchange_value': product_exchange_value,
                'transaction_id': transaction_id,
                'bonus': bonus,
                'message': 'Fault Tolerance is OFF'
            }), 200

if __name__== '__main__':
    app.run(host='0.0.0.0', port=5050)