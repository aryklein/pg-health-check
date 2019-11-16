#!/usr/bin/python

import psycopg2
from flask import Flask, g, make_response
from gevent.pywsgi import WSGIServer
import http
import argparse
import signal
import logging
import sys

app = Flask(__name__)

def handle_signal(signum, frame):
    logging.info('Stopping process... (signal {})'.format(signum))
    sys.exit(0)

def get_args():
    parser = argparse.ArgumentParser(description='Consul health check for Postgres')
    parser.add_argument('-U', '--user',
            dest='user',
            required=True,
            help='''
            Username to connect to the database.
            '''
    )
    parser.add_argument('-P', '--password',
            dest='password',
            required=False,
            default='',
            help='''
            Username to connect to the database.
            '''
    )
    parser.add_argument('-H', '--host', 
            dest='host',
            required=True,
            help='''
            Postgres server or directory for the Unix-domain socket. Default Unix-domain socket directory.
            '''
    )
    parser.add_argument('-p', '--port', 
            dest='port',
            required=False,
            default='5432',
            help='''
            TCP port or local Unix-domain socket file extension on which the Postgres server is listening for connections. Default 5432
            '''
    )
    parser.add_argument('-w', '--wsport',
            dest='wsport',
            required=False,
            default='5000', 
            help='''
            TCP port where the web server is listening for connections. Default 5000.
            '''
    )
    arguments = vars(parser.parse_args())
    return arguments

@app.before_request
def get_db():
    db = g.get('db', None)
    if db is None:
        try:
            g.db = psycopg2.connect(user=args['user'], host=args['host'], port=args['port'], password=args['password'])
            g.cur = g.db.cursor()
        except psycopg2.Error:
            logging.error('Connection error')
            return make_response('Connection error', http.HTTPStatus.SERVICE_UNAVAILABLE)

@app.after_request
def close_connection(response):
    db = g.get('db', None)
    cur = g.get('cur', None)

    try:
        if cur is not None:
            cur.close()
        if db is not None:
            db.close()
    except psycopg2.Error:
        pass
    finally:
        return response

@app.route('/health', methods=['GET'])
def health():
    cur = getattr(g, 'cur', None)
    try:
        cur.execute('SELECT 1')
        record = cur.fetchone()
        if record == (1,):
            logging.info('Service healthy')
            return make_response('OK', http.HTTPStatus.OK)
        else:
            return make_response('Postgres error', http.HTTPStatus.INTERNAL_SERVER_ERROR)
    except psycopg2.Error:
        return make_response('Postgres error', http.HTTPStatus.SERVICE_UNAVAILABLE)


logging.basicConfig(level=logging.DEBUG)
signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)
args = get_args()
logging.info('Staring process...')
http_server = WSGIServer(('0.0.0.0', int(args['wsport'])), app)
http_server.serve_forever()
