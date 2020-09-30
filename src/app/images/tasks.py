import socket
import json

from app import celery
import utils
import settings


@celery.task()
def get_images(auth_token):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    token = {'token': auth_token}
    pck = utils.create_packet(utils.IMAGES_GET, data=json.dumps(token).encode())
    sock_server.sendall(pck)

    res_pck = utils.read_data_from_socket(sock_server)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return res


@celery.task()
def store_image(auth_token, name, file_data, nodetype_id):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    data = {'token': auth_token, 'image_name': name, 'image_data': file_data, 'nodetype_id': nodetype_id}
    pck = utils.create_packet(utils.IMAGE_SAVE, data=json.dumps(data).encode())
    sock_server.sendall(pck)

    res_pck = utils.read_data_from_socket(sock_server)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return res


@celery.task()
def delete_image(auth_token, name):
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((settings.SERVER_IP, int(settings.SERVER_PORT)))

    data = {'token': auth_token, 'image_name': name}
    pck = utils.create_packet(utils.IMAGE_DELETE, data=json.dumps(data).encode())
    sock_server.sendall(pck)
    res_pck = utils.read_data_from_socket(sock_server)
    if res_pck:
        res = utils.segment_packet(res_pck)
    else:
        res = {'status': 500}
    sock_server.close()

    return res
