from flask import Blueprint, request, jsonify

from app.timeslots.tasks import save_timeslots, get_date_slots, get_user_slots
import utils


timeslots_bp = Blueprint('timeslots', __name__, url_prefix='/api/timeslots')


@timeslots_bp.route("/", methods=['POST'])
def save():
    # { slots: [{start, end}] }
    #
    # OnSuccess: { slots: [{start, end}], status: 200 }
    # OnError  : { message, status: 401 }
    #            { status: 500 }

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'message': 'Missing TOKEN'}), 401

    task = save_timeslots.apply_async(args=[auth_token, request.data.decode()])
    res = task.wait()

    status = res.pop('status')
    return jsonify(res), status


@timeslots_bp.route("/day", methods=['GET'])
def day_slots():
    # { date }
    #
    # OnSuccess: [{start, end, user_id}],   200
    # OnError  : message,                   401
    #            {},                        500

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'message': 'Missing TOKEN'}), 401

    task = get_date_slots.apply_async(args=[auth_token, request.args.to_dict()])
    res = task.wait()

    status = res.pop('status')
    return jsonify(res), status


@timeslots_bp.route("/user", methods=['GET'])
def user_slots():
    #
    #
    # OnSuccess: [{slot_id, start, end}],   200
    # OnError  : message,                   401
    #            {},                        500

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'message': 'Missing TOKEN'}), 401

    task = get_user_slots.apply_async(args=[auth_token])
    res = task.wait()

    status = res.pop('status')
    return jsonify(res), status
