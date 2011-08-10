#!/usr/bin/python

# File        : worker.py
# Description : Implements the worker module for MQ

import pika
import json

from web_utils import WebPage


def processURL(URL):
    webHandle = WebPage(URL)
    data = webHandle.crawlWebPage()
    print data

def callback(channel, method, properties, body):
    body = json.loads(body)
    [processURL(URL) for URL in body]

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host = 'localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='active')
    print "Starting Worker..."
    channel.basic_consume(callback, queue='active', no_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    main()

