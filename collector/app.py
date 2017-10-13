import os
import json
import time
import utils
import logging
import datetime

logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CONSUME = os.getenv('CONSUME')


def callback(ch, method, properties, body):
    data = json.loads(body)

    logger.info('Started processing content. {}'.format(data['pipeline_key']))

    process(data)

    logger.info('Done writing an event. {}'.format(data['pipeline_key']))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def process(data):
    key = '<unknown>'
    try:
        key = data['pipeline_key']
        logger.info('Got results for {}'.format(key))

        root = '/src/data/'
        now = datetime.datetime.utcnow().strftime('%Y/%m/%d')
        path = os.path.join(root, now)

        if not os.path.exists(path):
            os.makedirs(path)

        fname = '{}.json'.format(key)
        with open(os.path.join(path, fname), 'w') as f:
            f.write(json.dumps(data))
    except:
        # If something goes wrong, log it and return nothing
        logger.exception('Failed to write results for {}'.format(key))
        # Make sure to update this line if you change the variable names


def main():
    logger.info('... waiting ...')
    time.sleep(30)
    logger.info('... done ...')

    rabbit_consume = utils.RabbitClient(queue=CONSUME,
                                        host='rabbitmq')

    rabbit_consume.receive(callback)


if __name__ == '__main__':
    logger.info('Running...')
    main()
