import json
import os

import pika


def send_to_exchange(data):
    """ Dispatch msg for all projects listen this exchange """
    connection = pika.BlockingConnection(pika.URLParameters(os.getenv('RABBIT_HOST')))
    channel = connection.channel()

    channel.exchange_declare(exchange='news_exchange', exchange_type='fanout')

    msg = json.dumps(data)

    channel.basic_publish(exchange='news_exchange', routing_key='', body=msg)

    print(f"Msg was send to RabbitMQ: {msg}")
    connection.close()
