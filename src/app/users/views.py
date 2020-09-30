from flask import Blueprint, request, jsonify

from app.users.tasks import user_signup, user_login


users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route("/", methods=['POST'])
def signup():
    # {email, username, password}
    #
    # OnSuccess: {},        201
    # OnError  : message,   401
    #            {},        500

    task = user_signup.apply_async(args=(request.data.decode(), ))
    res = task.wait()

    status = res.pop('status')
    return jsonify(res), status


@users_bp.route("/login", methods=['POST'])
def login():
    # {email, password}
    #
    # OnSuccess: token,     200
    # OnError  : message,   401
    #            {},        500

    task = user_login.apply_async(args=(request.data.decode(), ))
    res = task.wait()

    status = res.pop('status')
    return jsonify(res), status
