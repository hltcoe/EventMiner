import os
import time
import json
import utils
import logging
import requests
import datetime
from copy import deepcopy
from dateutil.parser import parse

logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

cwd = os.path.abspath(os.path.dirname(__file__))


def callback(ch, method, properties, body):
    data = json.loads(body)
    logger.info('Started processing content. {}'.format(data['pipeline_key']))

    extract(data)

    logger.info('Finished PETR extracting. {}'.format(data['pipeline_key']))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def extract(message):
    publish = 'actors'
    rabbit_publish = utils.RabbitClient(queue=publish,
                                        host='rabbitmq')

    story = message

    keys = story['event_info'].keys()
    #keys = [k for k in keys if k != 'predicted_relevancy']
    for val in keys:
        logger.info('Processing {}'.format(val))
        text = story['event_info'][val]['sent']
        text = text.encode('utf-8')

        event_dict = send_to_corenlp(story, text)

        try:
            events_r = send_to_petr(event_dict)
        except Exception as e:
            logger.info('There was an exception with PETR. {}\n'.format(e))
            events_r = {}
        try:
#            event_updated = process_results(events_r.json())
            event_updated = events_r.json()

            story['event_info'][val]['coded'] = []
            for e in event_updated:
                if e:
                    story['event_info'][val]['coded'].append(e)
                else:
                    pass

            #logger.info(json.dumps(story))
        except Exception as e:
            logger.info(json.dumps(events_r.json()))
            logger.info('Something went wrong in the formatting. {}\n'.format(e))
            pass

    rabbit_publish.send(story, publish)


def send_to_petr(event_dict):
    headers = {'Content-Type': 'application/json'}

    events_data = json.dumps({'events': event_dict})
    petr_url = 'http://petrarch:5001/petrarch/code'
    events_r = requests.post(petr_url, data=events_data, headers=headers)

    return events_r


def send_to_corenlp(story, text):
    storyid = story['pipeline_key']
    try:
        date = story['date']
        date = parse(date).strftime('%Y%m%d')
    except Exception as e:
        logger.info('Error occured with the date.')
        date = datetime.datetime.utcnow().strftime('%Y%m%d')

    headers = {'Content-Type': 'application/json'}
    core_data = json.dumps({'text': text})
    ccnlp_url = 'http://ccnlp:5000/process'
    r = requests.post(ccnlp_url, data=core_data, headers=headers)
    out = r.json()

    event_dict = process_corenlp(out, date, storyid)

    return event_dict


def process_corenlp(output, date, STORYID):
    event_dict = {STORYID: {}}
    event_dict[STORYID]['sents'] = {}
    event_dict[STORYID]['meta'] = {}
    event_dict[STORYID]['meta']['date'] = date
    for i, sent in enumerate(output['sentences']):
        sents = output['sentences']
        event_dict[STORYID]['sents'][str(i)] = {}
        event_dict[STORYID]['sents'][str(i)]['content'] = ' '.join(sents[i]['tokens'])
        event_dict[STORYID]['sents'][str(i)]['parsed'] = sents[i]['parse'].upper().replace(')', ' )')

    return event_dict


def process_results(event_dict):
    new_event_dict = deepcopy(event_dict)
    for s_id in event_dict:
        sents = event_dict[s_id]['sents']
        for sent in sents:
            if 'events' not in sents[sent].keys():
                del new_event_dict[s_id]['sents'][sent]
            else:
                del new_event_dict[s_id]['sents'][sent]['parsed']
            if 'issues' not in sents[sent].keys():
                sents[sent]['issues'] = []

    return new_event_dict


def main():
    logger.info('... waiting ...')
    time.sleep(60)
    logger.info('... done ...')

    consume = 'quad'
    rabbit_consume = utils.RabbitClient(queue=consume,
                                        host='rabbitmq')

    rabbit_consume.receive(callback)


if __name__ == '__main__':
    logger.info('Running...')
    main()
