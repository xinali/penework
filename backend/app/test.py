#encoding:utf-8 

from flask import Flask, request, jsonify
import jwt
import time

def auth_token(func):
    
    def wrapper(*args, **kwargs):
        token  =  request.headers['token']
        if token == 'nimei':
            return jsonify({"test":"success"})
        # decode_token = jwt.decode(token, 'test', algorithm='HS256')
        # if (int(time.time()) - decode_token['time']) > Config.EXPIRE_TIME
            # return jsonify({'code':5001, 'message': 'Token Expire Time!'})
        return func(*args, **kwargs)

    return wrapper


app = Flask(__name__)

@app.route('/')
@auth_token
def index():
    print request.headers['token']
    return jsonify({'test': 'this is in index'})

from redis import Redis
from rq import Queue
from scan_worker import scan

r = Redis(host='192.168.123.4', port=6379, db=0)
print r 

q = Queue(connection=r)

if __name__ == '__main__':
    print 'q_len:', len(q)
    job = q.enqueue(scan)
    print 'q_len:', len(q)
    print job.result
    time.sleep(5)
    print job.result
