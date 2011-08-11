#!/usr/bin/python

# File        : worker.py
# Description : Implements the worker module for MQ

import pika
import json

from web_utils import WebPage

def processURL(URL):
    webHandle = WebPage(URL)
    links = webHandle.crawlWebPage()
    dump = json.dumps(links)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host = 'localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='active')
    channel.basic_publish(exchange='',
                          routing_key='active',
                          body=dump)
    
def callback(channel, method, properties, body):
    body = json.loads(body)
    [processURL(URL) for URL in body]
    channel.basic_ack(delivery_tag = method.delivery_tag)
    
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host = 'localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='active')
    print "Starting Worker..."
    channel.basic_consume(callback, queue='active')
    channel.start_consuming()
    
if __name__ == "__main__":
    main()

