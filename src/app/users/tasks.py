import socket

from app import celery
import utils
import settings


@celery.task()
def user_signup(data):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    pck = utils.create_packet(utils.USERS_SIGNUP, data=data.encode())
    sock_server.sendall(pck)

    res_pck = utils.read_data_from_socket(sock_server)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return res


@celery.task()
def user_login(data):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    pck = utils.create_packet(utils.USERS_LOGIN, data=data.encode())
    sock_server.sendall(pck)

    res_pck = utils.read_data_from_socket(sock_server)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return res
