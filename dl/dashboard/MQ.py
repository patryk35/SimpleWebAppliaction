import datetime
from shutil import copyfile

import pika
from gevent import os

from config.configuration import THUMBNAIL_PATH

exchange = '284930-pm-pi-2018-queue'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='284930-pm-pi-2018-queue', exchange_type='topic')


def create_thumbnail(file_path, file_extension):
    img_extensions = ["jpg", "jpeg", "gif", "png"]

    if file_extension not in img_extensions:
        return ""

    origin_thumbnail_path = THUMBNAIL_PATH + "." + file_extension
    thumbnail_path = os.path.abspath(file_path + ".thumbnail." + file_extension)
    copyfile(origin_thumbnail_path, thumbnail_path)
    thumbnail_name = thumbnail_path.split("/")[-1]

    routing_key = "resize." + file_extension
    channel.basic_publish(exchange=exchange,
                          routing_key=routing_key,
                          body=thumbnail_path)
    print("[" + str(datetime.datetime.today()) + "][RabbitMQ " + exchange + "][routing_key=" + routing_key + "] Sent '" + thumbnail_path + "'")
    return thumbnail_name
