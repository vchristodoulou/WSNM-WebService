import os

from flask import Blueprint, request, jsonify, after_this_request, send_from_directory

from app.debug.tasks import start_debug_channel, end_debug_channel, clear_log, download_log
import utils


debug_bp = Blueprint('debug', __name__, url_prefix='/api/debug')


@debug_bp.route("/start", methods=['POST'])
def start():
    # { slot_id }
    #
    # OnSuccess: { task_id, status: 200 }
    # OnError  : { message, status: 401 }
    #            { status: 500 }

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'status': 'FAIL', 'message': 'Missing TOKEN'}), 401

    task = start_debug_channel.apply_async(args=[auth_token, request.data.decode()])

    return jsonify({'task_id': task.id}), 200


@debug_bp.route("/end", methods=['POST'])
def end():
    # { slot_id }
    #
    # OnSuccess: { status: 204 }
    # OnError  : { message, status: 401 }
    #            { status: 500 }

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'status': 'FAIL', 'message': 'Missing TOKEN'}), 401

    task = end_debug_channel.apply_async(args=[auth_token, request.data.decode()])
    res = task.wait()

    status = res.pop('status')
    return jsonify(res), status


@debug_bp.route("/clear_log", methods=['POST'])
def clear():
    # { slot_id }
    #
    # OnSuccess: { status: 204 }
    # OnError  : { message, status: 401 }
    #            { status: 500 }

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'status': 'FAIL', 'message': 'Missing TOKEN'}), 401

    task = clear_log.apply_async(args=[auth_token, request.data.decode()])
    res = task.wait()

    status = res.pop('status')
    return jsonify(res), status


@debug_bp.route("/download_log", methods=['POST'])
def download():
    # { slot_id }
    #
    #
    # OnError  : { message, status: 401 }
    # OnError  : { message, status: 403 }
    #          : { status: 500 }


    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'status': 'FAIL', 'message': 'Missing TOKEN'}), 401

    task = download_log.apply_async(args=[auth_token, request.data.decode()])
    _dir, name = task.wait()

    @after_this_request
    def remove_file(response):
        try:
            os.remove(_dir + '/' + name)
        except OSError:
            print('Could not remove file', _dir + '/' + name)
            pass
        return response

    return send_from_directory(_dir, filename=name, as_attachment=True)

