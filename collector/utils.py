import pika
import json


class RabbitClient(object):
    def __init__(self, queue, host='localhost'):
        self.queue = queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.queue, durable=True)

    def send(self, n, routing):
        self.channel.basic_publish(exchange='',
                                   routing_key=routing,
                                   properties=pika.BasicProperties(
                                            delivery_mode=2,),
                                   body=json.dumps(n))

    def receive(self, callback):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(callback, queue=self.queue)
        self.channel.start_consuming()
