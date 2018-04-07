#encoding:utf-8 

import os 
import requests
import jwt
import time

from flask_mongoengine import MongoEngine
from flask import Flask, url_for, request, redirect, render_template, \
                  make_response, request, jsonify
from flask_security import Security, MongoEngineUserDatastore, \
                  UserMixin, RoleMixin, login_required,  LoginForm, \
                  url_for_security, current_user, login_user

from models import Users, Roles
from lib.utils.store import hashpasswd
from lib.core.config import Config
from lib.utils.init import initdb
from lib.core.log import logger 
from lib.core.db import mongo

# some init 
# register logger/init db and so on

db = MongoEngine()
app = Flask(__name__)
app.config.from_object(Config)

# flask_security config
user_datastore =  MongoEngineUserDatastore(db, Users, Roles)
security = Security(app, user_datastore)

db.init_app(app)

@app.before_first_request
def create_user_role():
    try:
        # create admin user
        admin = user_datastore.create_user(username='admintest', password=hashpasswd('admintest'))
        # create User role
        user_role = user_datastore.create_role(name='User', description='Generic user role')
        # create Admin role
        admin_role = user_datastore.create_role(name='Admin', description='Admin user role')
        user_datastore.add_role_to_user(admin, admin_role)
        # db.session.commit()
    except Exception as ex:
        logger.exception(ex.message)


def auth_token(func):
    def wrapper(*args, **kwargs):
        try:
            token = ''
            if request.headers['token']:
                token  =  request.headers['token']
                decode_token = jwt.decode(token, Config.TOKEN_KEY, algorithm='HS256')
                if (int(time.time()) - decode_token['time']) > Config.EXPIRE_TIME:
                    return jsonify({'code':5001, 'message': 'Token Expire Time!'})
        except Exception as ex:
            logger.exception(ex.message)
            return jsonify({'code': 5002, 'message': 'Toke is not athorithed or no token!'})
        return func(*args, **kwargs)

    return wrapper


@app.route('/api/login', methods=['post'])
def Login():
    if request.form.get('username') and request.form.get('password'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.objects(username=username).first()
        if user is None:
            # return make_response(jsonify({'error': 'Username or password is wrong!'}), 400)
            return jsonify({'code': 4000, 'message': 'Username or password is wrong!'})
        if not user.password == hashpasswd(password):
            print user.password, password
            print user.password, hashpasswd(password)
            # return make_response(jsonify({'error': 'Username or password is wrong!'}), 400)
            return jsonify({'code':4000, 'message': 'Username or password is wrong!'})
        
        login_user(user)
        time_ = int(time.time())
        token = jwt.encode({'time':time_}, Config.TOKEN_KEY, algorithm='HS256')
        return jsonify({'token':token})
    else:
        return jsonify({'code':6000, 'message': 'Username or password is wrong!'})
        # return make_response(jsonify({'error': 'Username or password is wrong!'}), 400)


@app.route('/api/project/list', methods=['get', 'post'])
@login_required
@auth_token
def ProjectList():
    try:
        projects = []
        for project in mongo[Config.MONGODB_C_PROJECTS].find():
            projects.append(project)
        return jsonify({'code':2000, 'rdata': projects})
    except Exception as ex:
        logger.exception(ex.message)
        return jsonify({'code': 6000, 'message': 'Get project list error!'})


@app.route('/api/project/add', methods=['post'])
@login_required
@auth_token 
def ProjectAdd():
    try:
        pid = request.data['pid']
        running_pro = mongo[Config.MONGODB_C_PROJECTS].find({'status': 'running'}).count()
        if running_pro > Config.MSCAN_RUNNING:
            # don't start masscan
            pass

        mongo[Config.MONGODB_C_PROJECTS].insert(request.data)
    except Exception as ex:
        logger.exception(ex.message)
        return jsonify({'code': 6000, 'message': 'Add project error'})
    

@app.route('/api/project/delete', methods=['post'])
@login_required
@auth_token 
def ProjectDelete():
    # delete project if not running
    # stop then delete if project is running
    try:
        pass
    except Exception as ex:
        logger.exception(ex.message)


@app.route('/api/project/update', methods=['post'])
@login_required
@auth_token 
def ProjectUpdate():
    try:
        pass
    except Exception as ex:
        logger.exception(ex.message)


@app.route('/api/portinfo', method=['pid'])
@login_required
@auth_token
def PortInfo():
    try: 
        infos = []
        pid = request.data['pid']
        for info in mongo[Config.MONGODB_C_NSCAN].find({'pid':pid}):
            infos.append(info)
        return jsonify({'code': 2000, 'rdata': infos})
    except Exception as ex:
        logger.exception(ex.message)
        return jsonify({'code': 6000, 'message': 'Get ports info error!'})


@app.route('/api/subdomain')
@login_required
@auth_token
def SubDomain():
    try:
        pass
    except Exception as ex:
        logger.exception(ex.message)
