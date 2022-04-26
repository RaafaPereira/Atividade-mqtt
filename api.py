#Rafael Pereira - 587761

import time
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
async_mode = None
from flask_socketio import SocketIO, send, emit

app = Flask(__name__, template_folder='templates')
CORS(app, support_credentials=True)
socketio = SocketIO(app, async_mode=async_mode)

arrayRequests = []
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/get-messages', methods=["GET"])
@cross_origin(supports_credentials=True)
def getMessages():
    global arrayRequests
    time.sleep(10)
    return jsonify(arrayRequests)

@app.route('/notificar', methods=["POST"])
def saveMessages():
    global arrayRequests
    arrayRequests.append(request.json)
    with app.app_context():
        socketio.emit("on_message", request.json, namespace='/messages')
    return request.json

@socketio.on('on_connect', namespace='/messages')
def on_connect(message):
    print('conectou')

@socketio.on('on_message', namespace='/messages')
def on_message(message):
    print('conectou')
    send(message)

app.run(debug=True)