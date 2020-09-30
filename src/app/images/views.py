from flask import Blueprint, request, jsonify

from app.images.tasks import get_images, store_image, delete_image
import utils


images_bp = Blueprint('images', __name__, url_prefix='/api/images')


@images_bp.route("/", methods=['GET'])
def retrieve():
    # OnSuccess: { data: [{ nodetype_id, images }], status: 200 }
    #            {},            500

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'message': 'Missing TOKEN'}), 401

    task = get_images.apply_async(args=[auth_token])
    res = task.wait()

    status = res.pop('status')
    return jsonify(res), status


@images_bp.route("/<file_name>", methods=['POST'])
def save(file_name):
    # OnSuccess: {},    200
    #            {},    500

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'message': 'Missing TOKEN'}), 401

    file_data = request.files['binary'].read()
    task = store_image.apply_async(args=[auth_token, file_name, file_data.decode(), request.form['nodetype_id']])
    res = task.wait()

    status = res.pop('status')
    return jsonify(res), status


@images_bp.route("/<file_name>", methods=['DELETE'])
def delete(file_name):
    # OnSuccess: {},    204
    #            {},    500

    auth_token = utils.get_token_from_header(request.headers.get('Authorization'))
    if not auth_token:
        return jsonify({'message': 'Missing TOKEN'}), 401

    task = delete_image.apply_async(args=[auth_token, file_name])
    res = task.wait()

    status = res.pop('status')
    return jsonify(res), status
