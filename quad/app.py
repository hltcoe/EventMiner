import os
import json
import utils
import logging

logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


MAXLEN = 1400
CONSUME = os.getenv('CONSUME')
PUBLISH = os.getenv('PUBLISH')


def callback(ch, method, properties, body):
    global MODEL, VOCAB, VOCAB_SIZE, CHECK
    data = json.loads(body)
    if data['predicted_relevancy'] == 1:
        logger.info('Started processing content. {}'.format(data['pipeline_key']))

        process(data, MODEL, VOCAB, VOCAB_SIZE, CHECK)

        logger.info('Finished quad tagging. {}'.format(data['pipeline_key']))
    else:
        logger.info('Irrelevant content. {}'.format(data['pipeline_key']))
        pass
    ch.basic_ack(delivery_tag=method.delivery_tag)


def process(data, model, vocab, vocab_size, check):
    rabbit_publish = utils.RabbitClient(queue=PUBLISH,
                                        host='rabbitmq')

    sents = data['sents']
    data['event_info'] = {}
    for sid, sent in sents.iteritems():
        try:
            logger.info('Processing sent {} for content {}'.format(sid,
                                                                   data['pipeline_key']))
            mat = utils.encode_data([sent['text']], MAXLEN, vocab, vocab_size, check)
            pred = model.predict(mat)
            pred_class = pred.argmax(1)[0]
            pred_score = pred[0][pred_class]
            data['event_info'][sid] = {}
            data['event_info'][sid]['predicted_class'] = {'class': pred_class,
                                                          'score': str(pred_score)}
            data['event_info'][sid]['sent'] = sent
        except Exception as e:
            # If something goes wrong, log it and return nothing
            logger.info(e)
            # Make sure to update this line if you change the variable names
            data['event_info'][sid] = {}
            data['event_info'][sid]['predicted_class'] = {}

    rabbit_publish.send(data, PUBLISH)


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
