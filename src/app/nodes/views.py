from flask import Blueprint, request, jsonify

from app.nodes.tasks import get_nodes, flash_nodes, reset_nodes, erase_nodes
import utils


nodes_bp = Blueprint('nodes', __name__, url_prefix='/api/nodes')


@nodes_bp.route("/", methods=['GET'])
def retrieve():
    # {}
    #
    # OnSuccess: { nodes, status: 200 }
    # OnError  : { message, status: 401 }
    #            { status: 500 }

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'message': 'Missing TOKEN'}), 401

    task = get_nodes.apply_async(args=[auth_token])
    res = task.wait()

    status = res.pop('status')
    return jsonify(res), status


@nodes_bp.route("/flash", methods=['POST'])
def flash():
    # { slot_id, image_name, node_uids }
    #
    # OnSuccess: { task_id, status: 200 }
    # OnError  : { message, status: 401 }
    #            { }

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'message': 'Missing TOKEN'}), 401

    task = flash_nodes.apply_async(args=[auth_token, request.data.decode()])

    return jsonify({'task_id': task.id}), 200


@nodes_bp.route("/erase", methods=['POST'])
def erase():
    # { slot_id, node_uids }
    #
    # OnSuccess: { task_id, status: 200 }
    # OnError  : { message, status: 401 }
    #            { }

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'message': 'Missing TOKEN'}), 401

    task = erase_nodes.apply_async(args=[auth_token, request.data.decode()])

    return jsonify({'task_id': task.id}), 200


@nodes_bp.route("/reset", methods=['POST'])
def reset():
    # { slot_id, node_uids }
    #
    # OnSuccess: { }
    # OnError  : { message, status: 401 }
    #            { }

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'message': 'Missing TOKEN'}), 401

    task = reset_nodes.apply_async(args=[auth_token, request.data.decode()])
    res = task.wait()

    status = res.pop('status')
    return jsonify(res), status

