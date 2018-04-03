#encoding:utf-8 

from flask import Flask, request, jsonify
import jwt

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

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8070, debug=True)