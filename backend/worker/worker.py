import redis
from rq import Connection, Worker

#REDIS_URL = 'redis://127.0.0.1'
REDIS_URL = 'redis://redis:6379/0'

def run_worker():
    redis_url = REDIS_URL
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        #worker = Worker.count(connection = redis_connection)
        worker = Worker.all()
        worker = Worker(['default'])
        #print(worker)
        worker.work()

run_worker()