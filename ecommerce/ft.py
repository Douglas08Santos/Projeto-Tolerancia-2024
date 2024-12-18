from email import message
import json
import random
import time
from urllib import response
import docker
from flask import jsonify
import pika
import requests

latest_usd_exchange_rate = 1.0

RABBITMQ_HOST = 'rabbitmq'

def ft_seek_product(product_id):
    try:
        # Request para Store, via get
        response = requests.get('http://store:5001/product', params={'product': product_id})

        #Verificação se o produto foi encontrado
        if response.status_code == 200: #OK
            product = response.json()
            return {
                'product': product, 
                'status_code':response.status_code
            } 
        else:
            return {
                'message': response.json()['message'], # not found 404
                'status_code': response.status_code
            }
    except requests.exceptions.RequestException:
        return {
                'message': 'Service Unavailable', 
                'status_code': 503
            }
#keep alived
# Balanceador de carga
def ft_get_exchange():
   
    # tentando em exchange1
    try:
         # Simular falha de 'Stop', com taxa de 10%, o exchange1 será parado
        if random.random() < 0.1:
            raise requests.exceptions.ConnectionError
        
        response = requests.get('http://nginx:80/exchange')
        if response.status_code == 200:
            data = response.json()
            latest_usd_exchange_rate = data['exchange_rate']
            print('exchange1 OK')
            return latest_usd_exchange_rate
        # implementar um catch para tratar a exceção (log)
    except requests.exceptions.ConnectionError:
        pass

    # se exchange1 falhar, o exchange2 será solicitado
    try:
        response = requests.get('http://nginx:80/exchange')
        if response.status_code == 200:
            data = response.json()
            latest_usd_exchange_rate = data['exchange_rate']
            print('exchange OK')
            return latest_usd_exchange_rate
        # implementar um catch para tratar a exceção (log)
    except requests.exceptions.RequestException:
        pass

    #Se ambos falharem, será enviado o ultimo valor salvo
    return latest_usd_exchange_rate

def ft_make_purchase(product_id):
    try:
        response = requests.post('http://store:5001/sell', json={'product': product_id})

        if response.status_code == 200:
            return {
                'transaction_id': response.json()['transaction_id'],
                'status_code': response.status_code
            } #, #Ta de sacanagem kkkkkkkkkkkkkk
        else: 
            return {
                'message': response.json()['message'],
                'status_code': response.status_code
            }
    except requests.exceptions.RequestException:
        return {
                'message': 'Service Unavailable', 
                'status_code': 503
            }
   
    
def ft_send_bonus(user_id, bonus):
    try:
        response = requests.post('http://fidelity:5003/bonus', json={"user": user_id, "bonus":bonus})
        if response.status_code == 200:
            return {
                'message': response.json()['message'],
                'bonus': response.json()['bonus'],
                'amount_bonus': response.json()['amount_bonus'],
                'status_code': response.status_code
            }  
        else: 
            return {
                'message': response.json()['message'],
                'status_code': response.status_code
            }
    except Exception as e:
        pub_message({"user": user_id, "bonus":bonus})
        return {
            'message': 'Failed to send bonus, added to queue',
            'status_code': 503
        }

# Implementação da fila de mensagens - RabbitMQ

# Publish
def pub_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='fidelity_queue', durable=True) # Declaração da fila
    channel.basic_publish(
        exchange='',
        routing_key='fidelity_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()    