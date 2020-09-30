import os

from flask import Flask
from flask_cors import CORS
from celery import Celery
from flask_socketio import SocketIO
# from gevent import monkey

from config import config


celery = Celery()
socketio = SocketIO()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('CONFIG', 'development')
    # Flask app initialization
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])

    from app.nodes.views import nodes_bp
    from app.images.views import images_bp
    from app.status.views import status_bp
    from app.timeslots.views import timeslots_bp
    from app.users.views import users_bp
    from app.nodetypes.views import nodetypes_bp
    from app.debug.views import debug_bp
    app.register_blueprint(nodes_bp)
    app.register_blueprint(images_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(timeslots_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(nodetypes_bp)
    app.register_blueprint(debug_bp)

    # Celery configuration
    celery.config_from_object(app.config)
    # Monkey patch for gevent with redis
    # monkey.patch_all()
    # SocketIO initialization
    socketio.init_app(app, cors_allowed_origins="*", message_queue='redis://localhost:6379/0')

    return app
