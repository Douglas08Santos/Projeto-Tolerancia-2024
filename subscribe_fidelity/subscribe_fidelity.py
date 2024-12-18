#Subscribe
import json
import time
#import docker
import pika
import requests
from pika.exceptions import AMQPConnectionError

# Não sei porque raios funciona passando o IP do container, mas não o DNS
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
FIDELITY_HOST = '172.27.0.2'

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

# def sub_messages():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
#     channel = connection.channel()
#     channel.queue_declare(queue='fidelity_queue', durable=True)
#     channel.basic_qos(prefetch_count=1)
#     channel.basic_consume(queue='fidelity_queue', on_message_callback=process_message)
#     print("Waiting messages...")
#     channel.start_consuming()

def sub_messages():
    while True:
        try:
            print(f"Attempting to connect to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}")
            connection = create_connection()
            channel = connection.channel()
            
            # Declare queue with explicit settings
            channel.queue_declare(
                queue='fidelity_queue',
                durable=True,
                arguments={
                    'x-message-ttl': 86400000,  # 24h TTL
                    'x-queue-type': 'classic'
                }
            )
            
            print("Queue declared successfully")
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue='fidelity_queue',
                on_message_callback=process_message,
                auto_ack=False
            )
            
            print("[*] Connected and waiting for messages")
            channel.start_consuming()
            
        except AMQPConnectionError as e:
            print(f"Connection error: {str(e)}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            time.sleep(5)

def create_connection():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials,
        connection_attempts=3,
        retry_delay=5,
        heartbeat=600
    )
    return pika.BlockingConnection(parameters)

if __name__ == '__main__':
    sub_messages()