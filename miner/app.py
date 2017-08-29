import os
import json
import uuid
import utils
import logging

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

PUBLISH = os.getenv('PUBLISH')


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


class MinerAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('data', type=dict, location='json')
        super(MinerAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()

        rabbit = utils.RabbitClient(queue=PUBLISH, host='rabbitmq')

        logger.info('Received data...')
        data = args['data']
        data = utils.prep_data(data)
        pipeline_key = str(uuid.uuid4())
        data['pipeline_key'] = pipeline_key

        logger.info('Sending to the downstream...')
        rabbit.send(data, PUBLISH)

        logging.info('Sent {}'.format(pipeline_key))
        return pipeline_key


api.add_resource(MinerAPI, '/EventMiner')


if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(6000)
    IOLoop.instance().start()
