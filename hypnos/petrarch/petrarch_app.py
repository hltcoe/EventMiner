import os
import logging
from petrarch2 import petrarch2
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from flask import Flask, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse

logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)
api = Api(app)

cwd = os.path.abspath(os.path.dirname(__file__))


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


class CodeAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('events', type=dict)
        super(CodeAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        event_dict = args['events']
        to_return = []

        try:
            event_dict_updated = petrarch2.do_coding(event_dict)
            k = event_dict_updated.keys()[0]
            try:
                to_return = event_dict_updated[k]['sents']['0']['events']
            except KeyError:
                logger.info('No events to process')
            except:
                logger.exception("An error occured")
        except:
            logger.exception("An error occurred")

        return to_return


api.add_resource(CodeAPI, '/petrarch/code')

if __name__ == '__main__':
    config = petrarch2.utilities._get_data('data/config/', 'PETR_config.ini')
    logger.info("reading config")
    petrarch2.PETRreader.parse_Config(config)
    logger.info("reading dicts")
    petrarch2.read_dictionaries()

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5001)
    IOLoop.instance().start()
