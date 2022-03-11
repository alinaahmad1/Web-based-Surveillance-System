import eventlet
import socketio
sio = socketio.Server()
app = socketio.WSGIApp(sio)

def connect(sid, environ):
    print('connect', sid)

def my_message(sid, data):
    print('message', data)

def disconnect(sid):
    print('disconnect', sid)
    
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)