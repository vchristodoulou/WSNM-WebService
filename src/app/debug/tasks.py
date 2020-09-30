import socket
import json
import os

from app import celery
from app import socketio
import utils
import settings


@celery.task(bind=True)
def start_debug_channel(self, auth_token, data):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    token = {'token': auth_token}
    data = utils.update_request_data(data, token)
    pck = utils.create_packet(utils.DEBUG_START, data=json.dumps(data).encode())
    sock_server.sendall(pck)

    while True:
        res_pck = utils.read_data_from_socket(sock_server, timeout=None)  # Wait for debug data
        if res_pck:
            res = utils.segment_packet(res_pck)
            if 'message' in res:
                socketio.emit('on_debug', res)
                sock_server.close()
                return
            else:
                socketio.emit('on_debug', res)
        else:
            sock_server.close()
            return


@celery.task()
def end_debug_channel(auth_token, data):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    token = {'token': auth_token}
    data = utils.update_request_data(data, token)
    pck = utils.create_packet(utils.DEBUG_END, data=json.dumps(data).encode())
    sock_server.sendall(pck)

    res_pck = utils.read_data_from_socket(sock_server)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return res


@celery.task()
def clear_log(auth_token, data):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    token = {'token': auth_token}
    data = utils.update_request_data(data, token)
    pck = utils.create_packet(utils.DEBUG_CLEAR_LOG, data=json.dumps(data).encode())
    sock_server.sendall(pck)

    res_pck = utils.read_data_from_socket(sock_server)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return res


@celery.task()
def download_log(auth_token, data):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    token = {'token': auth_token}
    data = utils.update_request_data(data, token)
    pck = utils.create_packet(utils.DEBUG_GET_LOG, data=json.dumps(data).encode())
    sock_server.sendall(pck)

    _dir = os.path.dirname(os.path.abspath(__file__)) + '/images'
    name = utils.get_and_store_log_file(sock_server, _dir, auth_token)
    sock_server.close()

    return _dir, name
