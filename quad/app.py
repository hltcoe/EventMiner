import json
import logging
import os
import utils

logging.basicConfig(format='%(levelname)s %(asc
                   
                   
                   )s %(filename)s %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


MAXLEN = 1400
CONSUME = os.getenv('CONSUME')
PUBLISH = os.getenv('PUBLISH')


def callback(ch, method, properties, body):
    global MODEL, VOCAB, VOCAB_SIZE, CHECK

    data = json.loads(body)
    key = data['pipeline_key']

    data['event_info'] = {}
    for sid, sent in data['sents'].iteritems():
        data['event_info'][sid] = {}
        data['event_info'][sid]['predicted_class'] = {}
        data['event_info'][sid]['sent'] = sent

    if data['predicted_relevancy'] == 1:
        logger.info('Started processing content. {}'.format(key))
        data = process(data, MODEL, VOCAB, VOCAB_SIZE, CHECK)
        logger.info('Finished quad tagging. {}'.format(key))
    else:
        logger.info('Irrelevant content. {}'.format(key))

    publish(data)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def process(data, model, vocab, vocab_size, check):
    sents = data['sents']
    key = data['pipeline_key']
    for sid, sent in sents.iteritems():
        try:
            logger.info('Processing sent {} for content {}'.format(sid, key))
            mat = utils.encode_data(
                [sent['text']], MAXLEN, vocab, vocab_size, check,
            )
            pred = model.predict(mat)
            pred_class = pred.argmax(1)[0]
            pred_score = pred[0][pred_class]
            data['event_info'][sid]['predicted_class'] = {
                'class': pred_class, 'score': str(pred_score),
            }
        except:
            logger.exception('Error during quad processing of {}'.format(key))
    return data


def publish(data):
    client = utils.RabbitClient(queue=PUBLISH, host='rabbitmq')
    client.send(data, PUBLISH)


def main():
    rabbit_consume = utils.RabbitClient(queue=CONSUME, host='rabbitmq')
    rabbit_consume.receive(callback)


if __name__ == '__main__':
    args = utils.parse_arguments()

    logger.info('Loading model...')
    MODEL, VOCAB = utils.load_model(args)
    VOCAB_SIZE = len(VOCAB.keys())
    CHECK = set(VOCAB.keys())

    main()
