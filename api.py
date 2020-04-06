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
from flask import Flask, jsonify, request, Response
from gevent.pywsgi import WSGIServer

BASE_DE_DATOS = [
    {
        "id": 1,
        "tiempo": 1586182998.944152,
        "descripcion": "Ancho de banda de la interfaz ETH-0",
        "tipo": "Ancho de banda",
        "medidas_parciales":{
            "valor": 0.5,
            "parametro": "velocidad",
        },
        "valida": 1,
        "Datos de direccionamiento": {
            "direccion IP": "8.8.8.8",
            "puerto": 80,
            "protocolo": "TCP",
        },
    },
    {
        "id": 2,
        "tiempo": 1586183000.944152,
        "descripcion": "Ancho de banda de la interfaz ETH-1",
        "tipo": "Ancho de banda",
        "medidas_parciales":{
            "valor": 0.5,
            "parametro": "velocidad",
        },
        "valida": 1,
        "Datos de direccionamiento": {
            "direccion IP": "7.7.7.7",
            "puerto": 100,
            "protocolo": "TCP",
        },
    },
    {
        "id": 3,
        "tiempo": 1586183998.944152,
        "descripcion": "Ancho de banda de la interfaz ETH-2",
        "tipo": "Ancho de banda",
        "medidas_parciales":{
            "valor": 0.5,
            "parametro": "velocidad",
        },
        "valida": 1,
        "Datos de direccionamiento": {
            "direccion IP": "9.9.9.9",
            "puerto": 90,
            "protocolo": "TCP",
        },
    },
]

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
def medida_get():
    """
            Función: medida_get
            Descripción: Esta función procesa una petición GET sobre la URL /test seguida de un número (por ejemplo /test/1)
            Retorno: Devuelve un JSON que contiene el resultado de la operación
    """

    # Se lee la petición
    logging.info('[/medida][GET] He recibido GET a método /medida')
    ident = request.args.get('id')
    if ident:
        logging.info('[/medida][GET] La petición indica un ident: {}'.format(ident))
    ip = request.args.get('ip')
    if ip:
        logging.info('[/medida][GET] La petición indica una ip: {}'.format(ip))
    puerto = request.args.get('port')
    if puerto:
        logging.info('[/medida][GET] La petición indica el puerto {}'.format(puerto))

    # Se recupera la información
    medidas = buscarMedida(ident=ident, ip=ip, puerto=puerto)

    # Se compone la respuesta
    respuesta = {medida["id"]: medida for medida in medidas}

    # Devuelve la respuesta en formato de intercambio JSON
    return jsonify(respuesta)


@app.route('/medida', methods=['POST'])
def medida_post():
    """
            Función: medida_post
            Descripción: Esta función procesa una petición POST sobre la URL /medida
            Retorno: Devuelve un código 200 si el recurso se ha alojado
    """

    # Se lee la petición
    logging.info('[/medida][GET] He recibido GET a método /medida')
    ident = request.args.get('id')
    if ident:
        logging.info('[/medida][POST] La petición indica un ident: {}'.format(ident))
    ip = request.args.get('ip')
    if ip:
        logging.info('[/medida][POST] La petición indica una ip: {}'.format(ip))
    puerto = request.args.get('port')
    if puerto:
        logging.info('[/medida][POST] La petición indica el puerto {}'.format(puerto))
    descripcion = request.args.get('descripcion')
    if descripcion:
        logging.info('[/medida][POST] La petición indica la descripcion {}'.format(descripcion))
    tipo = request.args.get('tipo')
    if tipo:
        logging.info('[/medida][POST] La petición indica el tipo {}'.format(tipo))
    valor = request.args.get('valor')
    if valor:
        logging.info('[/medida][POST] La petición indica el valor {}'.format(valor))
    parametro = request.args.get('parametro')
    if parametro:
        logging.info('[/medida][POST] La petición indica el parametro {}'.format(parametro))
    protocolo = request.args.get('protocolo')
    if protocolo:
        logging.info('[/medida][POST] La petición indica el protocolo {}'.format(protocolo))

    # Se busca un id
    nuevo_ident = ident
    medidas = buscarMedida(ident=ident)
    if len(medidas) > 0:
        nuevo_ident = len(BASE_DE_DATOS) + 1

    # Se compone la respuesta
    respuesta = crearMedida(ident=nuevo_ident,
                            descripcion=descripcion,
                            tipo=tipo,
                            valor=valor,
                            parametro=parametro,
                            ip=ip,
                            puerto=puerto,
                            protocolo=protocolo)

    # Devuelve la respuesta en formato de intercambio JSON
    return jsonify(respuesta)


@app.route('/medida', methods=['DELETE'])
def medida_delete():
    """
            Función: medida_delete
            Descripción: Esta función procesa una petición DELETE sobre la URL /medida
            Retorno: Devuelve un código 204 si se ha borrado
    """

    # Se lee la petición
    logging.info('[/medida][DELETE] He recibido GET a método /medida')
    ident = request.args.get('id')
    if ident:
        logging.info('[/medida][DELETE] La petición indica un ident: {}'.format(ident))
    ip = request.args.get('ip')
    if ip:
        logging.info('[/medida][DELETE] La petición indica una ip: {}'.format(ip))
    puerto = request.args.get('port')
    if puerto:
        logging.info('[/medida][DELETE] La petición indica el puerto {}'.format(puerto))

    # Se recupera la información
    medidas = buscarMedida(ident=ident, ip=ip, puerto=puerto)

    # Se borran las entradas encontradas
    for medida in medidas:
        medida_id = medida["id"]
        BASE_DE_DATOS.pop(medida_id)

    # Devuelve la respuesta
    return Response("Se ha eliminado el recurso", 204)


def buscarMedida(ident=None, ip=None, puerto=None):

    medidas_candidatas_ident = []
    medidas_candidatas_ip = []
    medidas_candidatas_puerto = []
    
    for medida in BASE_DE_DATOS:
        
        if ident:
            
            ident_medida = medida["id"]
            if str(ident) == str(ident_medida):
                medidas_candidatas_ident.append(medida)
        
        if ip:

            ip_medida = medida["Datos de direccionamiento"]["direccion IP"]
            if ip == ip_medida:
                medidas_candidatas_ip.append(medida)
        
        if puerto:

            puerto_medida = medida["Datos de direccionamiento"]["puerto"]
            if str(puerto) == str(puerto_medida):
                medidas_candidatas_puerto.append(medida)

    id_medidas = []
    for medida in medidas_candidatas_ident:
        medida_idet = medida["id"]
        id_medidas.append(medida_idet)
    for medida in medidas_candidatas_ip:
        medida_idet = medida["id"]
        id_medidas.append(medida_idet)
    for medida in medidas_candidatas_puerto:
        medida_idet = medida["id"]
        id_medidas.append(medida_idet)
    set_medidas = list(set(id_medidas))

    medidas = []
    for medida in BASE_DE_DATOS:
        for medida_ident in set_medidas:
            ident_medida_guardada = medida["id"]
            if ident_medida_guardada == medida_ident:
                medidas.append(medida)

    return medidas


def crearMedida(ident=None,
                descripcion="Desconocido",
                tipo="Desconocido",
                valor=0,
                parametro="Desconocido",
                ip="0.0.0.0",
                puerto="0",
                protocolo="Desconocido"):
    return {
        "id": ident,
        "tiempo": time.time(),
        "descripcion": descripcion,
        "tipo": tipo,
        "medidas_parciales": {
            "valor": valor,
            "parametro": parametro,
        },
        "valida": 1,
        "Datos de direccionamiento": {
            "direccion IP": ip,
            "puerto": puerto,
            "protocolo": protocolo,
        },
    }


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
