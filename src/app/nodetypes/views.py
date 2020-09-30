from flask import Blueprint, request, jsonify

from app.nodetypes.tasks import get_nodetypes
import utils


nodetypes_bp = Blueprint('nodetypes', __name__, url_prefix='/api/nodetypes')


@nodetypes_bp.route("/", methods=['GET'])
def retrieve():
    #
    #
    # OnSuccess: {nodetypes, status: 200 }
    # OnError  : { message, status: 401 }
    #            { status: 500 }

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'message': 'Missing TOKEN'}), 401

    task = get_nodetypes.apply_async(args=[auth_token])
    res = task.wait()

    status = res.pop('status')
    return jsonify(res), status
