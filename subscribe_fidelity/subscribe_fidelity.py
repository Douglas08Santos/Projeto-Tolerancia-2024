#Subscribe
import json
import time

import docker
import pika
import requests

# Não sei porque raios funciona passando o IP do container, mas não o DNS
RABBITMQ_HOST = '172.19.0.3'
FIDELITY_HOST = '172.19.0.6'

def process_message(ch, method, properties, body):
    message = json.loads(body)
    user_id = message['user']
    bonus = message['bonus']

    try:
        response = requests.post(f'http://{FIDELITY_HOST}:5003/bonus', json={"user": user_id, "bonus":bonus})
        if response.status_code == 200:
            print(f"bonus of user {user_id} OK")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            raise Exception(f"Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Error processing message: {e}")
        time.sleep(5)  # Aguarda antes de tentar novamente
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # Reinsere a mensagem na fila

def sub_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='fidelity_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='fidelity_queue', on_message_callback=process_message)
    print("Waiting messages...")
    channel.start_consuming()

if __name__ == '__main__':
    sub_messages()