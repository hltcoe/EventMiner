import json
import pika
import cPickle
import argparse
import numpy as np

from keras.models import model_from_json


def parse_arguments():
    parser = argparse.ArgumentParser(description='Run the category classifier \
                                     API.')
    parser._optionals.title = 'Options'
    parser.add_argument('-m', '--model_path',
                        help='Directory path for the classifier model.',
                        type=str, required=True)
    parser.add_argument('-w', '--weights_path',
                        help='Directory path for the model weights.',
                        type=str, required=True)
    parser.add_argument('-v', '--vocab_path',
                        help='Directory path for the classifier vocab.',
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
    model = model_from_json(json.load(open(args.model_path)))
    model.load_weights(args.weights_path)

    vocab = cPickle.load(open(args.vocab_path))

    return model, vocab


def encode_data(x, maxlen, vocab, vocab_size, check):
    #Iterate over the loaded data and create a matrix of size maxlen x vocabsize
    #In this case that will be 1014x69. This is then placed in a 3D matrix of size
    #data_samples x maxlen x vocab_size. Each character is encoded into a one-hot
    #array. Chars not in the vocab are encoded into an all zero vector.

    input_data = np.zeros((len(x), maxlen, vocab_size))
    for dix, sent in enumerate(x):
        counter = 0
        sent_array = np.zeros((maxlen, vocab_size))
        chars = list(sent.lower().replace(' ', ''))
        for c in chars:
            if counter >= maxlen:
                pass
            else:
                char_array = np.zeros(vocab_size, dtype=np.int)
                if c in check:
                    ix = vocab[c]
                    char_array[ix] = 1
                sent_array[counter, :] = char_array
                counter += 1
        input_data[dix, :, :] = sent_array

    return input_data
