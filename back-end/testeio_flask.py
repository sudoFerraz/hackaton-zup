from flask import Flask
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(msg):
    print ('Message: ' + msg)
    send(msg, broadcast=True)
    send(msg)
    emit(msg)

@socketio.on('test', '/test')
def testing():
    socketio.emit('test')

@app.route('/')
def index():
    return "ok"

#if __name__ == '__main__':
socketio.run(app)
