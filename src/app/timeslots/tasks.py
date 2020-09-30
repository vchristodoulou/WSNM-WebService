import socket
import json

from app import celery
import utils
import settings


@celery.task()
def save_timeslots(auth_token, slots):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    token = {'token': auth_token}
    data = utils.update_request_data(slots, token)
    pck = utils.create_packet(utils.TIMESLOTS_SAVE, data=json.dumps(data).encode())
    sock_server.sendall(pck)

    res_pck = utils.read_data_from_socket(sock_server)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return res


@celery.task()
def get_date_slots(auth_token, date):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    data = {}
    data.update({'token': auth_token})
    data.update(date)
    pck = utils.create_packet(utils.TIMESLOTS_GET_DAYSLOTS, data=json.dumps(data).encode())
    sock_server.sendall(pck)

    res_pck = utils.read_data_from_socket(sock_server)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return res


@celery.task()
def get_user_slots(auth_token):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    token = {'token': auth_token}
    pck = utils.create_packet(utils.TIMESLOTS_GET_USERSLOTS, data=json.dumps(token).encode())
    sock_server.sendall(pck)

    res_pck = utils.read_data_from_socket(sock_server)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return res
