import json
import time
import utils
import logging

logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CONSUME = os.getenv('CONSUME')
PUBLISH = os.getenv('PUBLISH')


def callback(ch, method, properties, body):
    global TFIDF, CLF
    data = json.loads(body)
    logger.info('Started processing content. {}'.format(data['pipeline_key']))

    process(data, TFIDF, CLF)

    logger.info('Finished tagging relevancy. {}'.format(data['pipeline_key']))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def process(data, tfidf, clf):
    rabbit_publish = utils.RabbitClient(queue=PUBLISH,
                                        host='rabbitmq')
    try:
        mat = tfidf.transform([data['title']])
        pred = clf.predict(mat)
        data['predicted_relevancy'] = pred[0]
        logger.info('Finished processing content.')
    except Exception as e:
        # If something goes wrong, log it and return nothing
        logger.info(e)
        # Make sure to update this line if you change the variable names

    rabbit_publish.send(data, publish)


def main():
    logger.info('... waiting ...')
    time.sleep(30)
    logger.info('... done ...')

    rabbit_consume = utils.RabbitClient(queue=CONSUME,
                                        host='rabbitmq')

    rabbit_consume.receive(callback)


if __name__ == '__main__':
    args = utils.parse_arguments()
    logger.info('Loading model...')
    CLF, TFIDF = utils.load_model(args)
    logger.info('Running...')
    main()
