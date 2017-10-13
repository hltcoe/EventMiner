import os
import json
import utils
import logging

import ParseyPredFace


logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


CONSUME = os.getenv('CONSUME')
PUBLISH = os.getenv('PUBLISH')


def callback(ch, method, properties, body):
    data = json.loads(body)
    logger.info('Started processing content. {}'.format(data['pipeline_key']))

    process(data)

    logger.info('Finished PP extraction. {}'.format(data['pipeline_key']))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def process(data):
    rabbit_publish = utils.RabbitClient(queue=PUBLISH,
                                        host='rabbitmq')
    data['predicate_info'] = {}
    for sid, sent in data['sents'].iteritems():
        try:
            output = ParseyPredFace.parse(sent['text'].encode('utf-8'))

            data['predicate_info'][sid] = output
        except Exception as e:
            # If something goes wrong, log it and return nothing
            logger.info(e)
            # Make sure to update this line if you change the variable names

    logger.info('Finished processing content.')

    rabbit_publish.send(data, PUBLISH)


def main():
    rabbit_consume = utils.RabbitClient(queue=CONSUME, host='rabbitmq')
    rabbit_consume.receive(callback)


if __name__ == '__main__':
    logger.info('Running...')
    main()
