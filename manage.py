from app import create_app
from flask_socketio import SocketIO, send

app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handleMessage(msg):
  send(msg, broadcast=True)

if __name__ == '__main__':
  socketio.run(app)