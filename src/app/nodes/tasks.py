import socket
import json

from app import celery
import utils
import settings


@celery.task()
def get_nodes(auth_token):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    token = {'token': auth_token}
    pck = utils.create_packet(utils.NODES_GET, data=json.dumps(token).encode())
    sock_server.sendall(pck)
    res_pck = utils.read_data_from_socket(sock_server)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return res


@celery.task(bind=True)
def flash_nodes(self, auth_token, data):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    self.update_state(state='PROGRESS',
                      meta={'current': 1, 'total': 100, 'status': 'Task started!'})

    token = {'token': auth_token}
    data = utils.update_request_data(data, token)
    pck = utils.create_packet(utils.NODES_FLASH, data=json.dumps(data).encode())
    sock_server.sendall(pck)

    res_pck = utils.read_data_from_socket(sock_server, timeout=200)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': res['data']}


@celery.task(bind=True)
def erase_nodes(self, auth_token, data):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    self.update_state(state='PROGRESS',
                      meta={'current': 1, 'total': 100, 'status': 'Task started!'})

    token = {'token': auth_token}
    data = utils.update_request_data(data, token)
    pck = utils.create_packet(utils.NODES_ERASE, data=json.dumps(data).encode())
    sock_server.sendall(pck)

    res_pck = utils.read_data_from_socket(sock_server, timeout=200)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': res['data']}


@celery.task()
def reset_nodes(auth_token, data):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    token = {'token': auth_token}
    data = utils.update_request_data(data, token)
    pck = utils.create_packet(utils.NODES_RESET, data=json.dumps(data).encode())
    sock_server.sendall(pck)

    res_pck = utils.read_data_from_socket(sock_server, timeout=200)
    if res_pck:
        res = utils.segment_packet(res_pck)
        res['status'] = 200
        print(res)
    else:
        res = {'status': 500}
    sock_server.close()

    return res
