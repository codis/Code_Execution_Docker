# Code taken and modified from:
# https://testdriven.io/blog/asynchronous-tasks-with-flask-and-redis-queue/

import redis
from rq import Queue, Connection
from flask import Flask, jsonify, request
from execute import create_task

#REDIS_URL = 'redis://127.0.0.1'
REDIS_URL = 'redis://redis:6379/0'
app = Flask(__name__)
app.config['REDIS_URL'] = REDIS_URL

@app.route('/enqueue', methods=['POST'])
def enqueue_execution():
    arg = request.form['arg']
    print(arg)

    with Connection(redis.from_url(app.config['REDIS_URL'])):
        q = Queue()
        task = q.enqueue(create_task, arg)

    response_object = {
        'status': 'success',
        'data': {
            'task_id': task.get_id()
        }
    }

    return jsonify(response_object), 202

if __name__ == '__main__':
    app.run(debug = True,  host='0.0.0.0', port = 5001)