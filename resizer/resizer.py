#!/usr/bin/env python
import pika
import sys

from gevent import os

exchange_name = '284930-pm-pi-2018-queue'
queue_name = sys.argv[1]
binding_keys = sys.argv[2:]
if not binding_keys:
    sys.stderr.write(
        "Binding key missing. Usage: %s [queue_name] [binding_key(multiple keys allowed)]...\n" % sys.argv[0])
    sys.exit(1)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange=exchange_name,
                         exchange_type='topic')

channel.queue_declare(queue=queue_name, exclusive=True)

for binding_key in binding_keys:
    channel.queue_bind(exchange=exchange_name,
                       queue=queue_name,
                       routing_key=binding_key)


def create_thumbnail(path_to_file, destination, delivery_tag):
    command = "/usr/bin/convert " + path_to_file + " -resize 64x64\! " + destination
    print("[" + queue_name + "] " + command)
    os.system(command)
    channel.basic_ack(delivery_tag=delivery_tag)


def callback(ch, method, properties, body):
    print("[" + queue_name + "]Received: " + body.decode())
    names = body.decode().split(".")
    create_thumbnail(names[0], body.decode(), method.delivery_tag)


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=False)

print(' [*] Waiting for logs. To exit press CTRL+C')
channel.start_consuming()
