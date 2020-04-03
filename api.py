#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import json
import os
import time
import logging
from datetime import datetime
import re
import argparse
import gevent
import time
import signal
from argparse import RawTextHelpFormatter
from flask import Flask, jsonify, request
from gevent.pywsgi import WSGIServer

BASE_DE_DATOS = {
    '1': {
        
    },
    '2': {
        
    }
}

# Aplicación Flask apara implementar los métodos de la API REST
app = Flask(__name__)
# Objeto que almacena los parametros leídos por línea de comandos
args = None


def signal_handler(sig, frame):
    """
            Función: signal_handler
            Descripción: Esta función se ejecuta cuando se pulsa ctrl+c y cierra el programa
            Retorno: Ninguno
    """
    sys.exit(0)


def parse_args():
    """
            Función: parse_args
            Descripción: Esta función lee los parámetros que se reciben por línea de comandos
            Parámetros: Ninguno
            Retorno: Ninguno.La variable global args se modifica dentro de la función
    """
    global args
    parser = argparse.ArgumentParser(description='Ejemplo de API REST',formatter_class=RawTextHelpFormatter)
    parser.add_argument('--ip', dest='ip', default='localhost',help='Dirección IP donde escucha peticiones la API')
    parser.add_argument('--port', dest='port', type=int, default=9090,help='Puerto donde escucha peticiones la API')
    parser.add_argument('--debug', dest='debug', default=False, action='store_true',help='Activar mensajes de debug')
    args = parser.parse_args()


@app.route('/medida', methods=['GET'])
def test_get_variable(id):
    """
            Función: test_get_variable
            Descripción: Esta función procesa una petición GET sobre la URL /test seguida de un número (por ejemplo /test/1)
            Retorno: Devuelve un JSON que contiene el resultado de la operación
    """

    # Se lee la petición
    logging.info('[/medida][GET] He recibido GET a método /medida')
    id = request.args.get('id')
    if id:
        logging.info('[/medida][GET] La petición indica un id: {}'.format(id))
    ip = request.args.get('ip')
    if ip:
        logging.info('[/medida][GET] La petición indica una ip: {}'.format(ip))
    port = request.args.get('port')
    if port:
        logging.info('[/medida][GET] La petición indica el port {}'.format(port))

    # Se compone la respuesta
    respuesta = {
        'result':'Ok'
    }

    # Devuelve la respuesta en formato de intercambio JSON
    return jsonify(respuesta)


@app.route('/medida', methods=['POST'])
def test_get_variable(id):
    """
            Función: test_get_variable
            Descripción: Esta función procesa una petición GET sobre la URL /test seguida de un número (por ejemplo /test/1)
            Retorno: Devuelve un JSON que contiene el resultado de la operación
    """

    # Se lee la petición
    logging.info('[/medida][GET] He recibido GET a método /medida')
    id = request.args.get('id')
    if id:
        logging.info('[/medida][GET] La petición indica un id: {}'.format(id))
    ip = request.args.get('ip')
    if ip:
        logging.info('[/medida][GET] La petición indica una ip: {}'.format(ip))
    port = request.args.get('port')
    if port:
        logging.info('[/medida][GET] La petición indica el puerto {}'.format(port))

    # Se compone la respuesta
    respuesta = {
        'result': 'Ok'
    }

    # Devuelve la respuesta en formato de intercambio JSON
    return jsonify(respuesta)


@app.route('/medida', methods=['DELETE'])
def test_get_variable(id):
    """
            Función: test_get_variable
            Descripción: Esta función procesa una petición GET sobre la URL /test seguida de un número (por ejemplo /test/1)
            Retorno: Devuelve un JSON que contiene el resultado de la operación
    """

    # Se lee la petición
    logging.info('[/medida][GET] He recibido GET a método /medida')
    id = request.args.get('id')
    if id:
        logging.info('[/medida][GET] La petición indica un id: {}'.format(id))
    ip = request.args.get('ip')
    if ip:
        logging.info('[/medida][GET] La petición indica una ip: {}'.format(ip))
    port = request.args.get('port')
    if port:
        logging.info('[/medida][GET] La petición indica el puerto {}'.format(port))

    # Se compone la respuesta
    respuesta = {
        'result': 'Ok'
    }

    # Devuelve la respuesta en formato de intercambio JSON
    return jsonify(respuesta)


if __name__ == '__main__':
  
    # Main section.
    parse_args()
    if args.debug:
        logging.basicConfig(level = logging.DEBUG, format = '[%(asctime)s %(levelname)s]\t%(message)s')
    else:
        logging.basicConfig(level = logging.INFO, format = '[%(asctime)s %(levelname)s]\t%(message)s')

    signal.signal(signal.SIGINT, signal_handler)

    logging.info('API  REST escuchando en {}:{}'.format(args.ip, args.port))
    # inicializar el servidor Web asociado a la API REST
    http_server = WSGIServer((args.ip, args.port), app)
    # arrancar el servidor
    http_server.serve_forever()
