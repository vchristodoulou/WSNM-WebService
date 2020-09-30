import os

from flask import send_from_directory

from app import create_app, socketio
import settings


app = create_app(settings.APP_SETTINGS)


@app.route('/')
@app.route('/login')
@app.route('/signup')
@app.route('/calendar')
@app.route('/calendar/<day>')
@app.route('/images')
@app.route('/slots')
@app.route('/slot/<id>')
@app.route('/debug')
def root():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)) + '/dist', 'index.html')


@app.route('/static/<path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)) + '/dist', path)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)) + '/dist', 'favicon.ico')


@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred [main.py] %s' % e, 500


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
