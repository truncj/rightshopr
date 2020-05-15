#!/usr/bin/env python
import json
from threading import Lock

import redis
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS

async_mode = None

app = Flask(__name__)

# app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins="*")

thread = None
thread_lock = Lock()

r = redis.Redis(
    host='redis',
    port=6379,
    password='',
    decode_responses=True)


def background_thread():
    count = 0
    while True:
        count += 1
        get_slots()
        slot_data = get_slots()
        socketio.emit('my_response',
                      {'data': slot_data})
        socketio.sleep(3)


def get_slots():
    slot_obj = r.hgetall('store_slots')
    return json.dumps(slot_obj)


@socketio.on('connect')
def test_connect():
    print('connected')
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


# if __name__ == '__main__':
#     socketio.run(app, debug=True, host='0.0.0.0', port=5000)
