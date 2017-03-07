import json
import uuid
import pika
import nltk.data


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


def prep_data(data):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sents = sent_detector.tokenize(data['content'].strip())
    sent_dict = {str(uuid.uuid4()): x for x in sents[:2]}
    data['sents'] = sent_dict

    return data
