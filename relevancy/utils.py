import pika
import json
import argparse

from sklearn.externals import joblib


def parse_arguments():
    parser = argparse.ArgumentParser(description='Run the relevancy classifier\
                                     API.')
    parser._optionals.title = 'Options'
    parser.add_argument('-m', '--clf_path',
                        help='Filepath for the classifier model.',
                        type=str, required=True)
    parser.add_argument('-tf', '--tfidf_path',
                        help='Filepath for the TFIDF model.',
                        type=str, required=True)
    return parser.parse_args()


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


def load_model(args):
    model = joblib.load(args.clf_path)
    tfidf = joblib.load(args.tfidf_path)

    return model, tfidf
