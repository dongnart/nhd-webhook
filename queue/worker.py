from redis import Redis
from rq import Worker, Queue, Connection

redis_conn = Redis()

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker([Queue()])
        worker.work()