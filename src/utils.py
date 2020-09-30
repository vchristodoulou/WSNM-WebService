import struct
import socket
import json


NODES_GET = 'NGE'.encode()
NODES_FLASH = 'NFL'.encode()
NODES_RESET = 'NRS'.encode()
NODES_ERASE = 'NER'.encode()

TIMESLOTS_SAVE = 'TSA'.encode()
TIMESLOTS_GET_DAYSLOTS = 'TGD'.encode()
TIMESLOTS_GET_USERSLOTS = 'TGU'.encode()

USERS_SIGNUP = 'USU'.encode()
USERS_LOGIN = 'ULI'.encode()

NODETYPES_GET = 'NTG'.encode()

IMAGE_SAVE = 'IMS'.encode()
IMAGES_GET = 'IMG'.encode()
IMAGE_DELETE = 'IMD'.encode()

DEBUG_START = 'DST'.encode()
DEBUG_END = 'DEN'.encode()
DEBUG_CLEAR_LOG = 'DCL'.encode()
DEBUG_GET_LOG = 'DGL'.encode()
USER_LOG = 'user.log'

SIZE_ACTION = 3
SIZE_OF_DATA = 2

ERROR = 'ERROR'
SUCCESS = 'SUCCESS'

SOCK_BUFSIZE = 1024
SOCK_TIMEOUT = 5


def create_packet(action, data=None):
    """Create a packet"""

    pck = bytearray()

    pck.extend(struct.pack('!' + str(SIZE_ACTION) + 's', action))
    pck.extend(struct.pack('!H', len(data)))
    pck.extend(data)

    return pck


def segment_packet(pck):
    """Segment a packet"""

    pck_size = struct.unpack('!H', bytes(pck[:SIZE_OF_DATA]))
    return (json.loads(pck[SIZE_OF_DATA:
                           SIZE_OF_DATA + pck_size[0]]))


def read_data_from_socket(s, timeout=SOCK_TIMEOUT):
    s.settimeout(timeout)
    buffer = b''

    while True:
        try:
            data = s.recv(SOCK_BUFSIZE)
            if data:
                buffer = buffer + data
                if len(buffer) >= SIZE_OF_DATA:
                    data_size = struct.unpack('!H', bytes(buffer[:SIZE_OF_DATA]))[0]

                    while data_size + SIZE_OF_DATA > len(buffer):
                        data = s.recv(SOCK_BUFSIZE)
                        if data:
                            buffer = buffer + data
                        else:
                            break
                    return buffer
        except socket.timeout as e:
            print(e)
            break

    return buffer


def get_and_store_log_file(s, _dir, token, timeout=SOCK_TIMEOUT):
    s.settimeout(timeout)

    with open(_dir + '/' + token, 'wb') as f:
        while True:
            try:
                data = s.recv(SOCK_BUFSIZE)
                if data:
                    if len(data) >= SIZE_OF_DATA:
                        data_size = struct.unpack('!H', bytes(data[:SIZE_OF_DATA]))[0]
                        data = data[SIZE_OF_DATA:]
                        data_read = len(data)
                        if data:
                            f.write(data)

                        while data_size > data_read:
                            data = s.recv(SOCK_BUFSIZE)
                            data_read = data_read + len(data)
                            if data:
                                f.write(data)
                            else:
                                break
                        break
            except socket.timeout as e:
                break

    return token


def get_token_from_header(auth_header):
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return ''


def insert_to_data(data, *elements):
    if data:
        data = json.loads(data)
    else:
        data = []

    return list(elements) + data


def update_request_data(data, *elements):
    if data:
        data = json.loads(data)
    else:
        data = {}
    data.update(*elements)

    return data


def separate_by_gateway_id(data):
    result = []

    gateway_ids = {}
    i = 0
    for item in data:
        if item['gateway_id'] not in gateway_ids:
            gateway_ids[item['gateway_id']] = i
            result.append([item['gateway_id']])
            result[i].append(item['node_uid'])
            i += 1
        else:
            index = gateway_ids[item['gateway_id']]
            result[index].append(item['node_uid'])

    return result
