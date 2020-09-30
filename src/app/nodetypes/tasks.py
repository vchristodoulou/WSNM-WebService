import socket
import json

from app import celery
import utils
import settings


@celery.task()
def get_nodetypes(auth_token):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    token = {'token': auth_token}
    pck = utils.create_packet(utils.NODETYPES_GET, data=json.dumps(token).encode())
    sock_server.sendall(pck)

    res_pck = utils.read_data_from_socket(sock_server)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return res
