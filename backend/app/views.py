# encoding:utf-8

import jwt
import time
from functools import wraps
# from IPython import embed

from flask_mongoengine import MongoEngine
from flask import Flask, request, redirect, request, jsonify
from flask_security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required, login_user

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
# logger.info('-' * 100 + app.config['MONGODB_DB'])

# flask_security config
user_datastore = MongoEngineUserDatastore(db, Users, Roles)
security = Security(app, user_datastore)

db.init_app(app)


@app.before_first_request
def create_user_role():
    # create admin user
    try:
        admin = None
        if user_datastore.get_user('adminwt0f'):
            pass
    except Exception as ex:
        # logger.exception(ex.message)
        admin = user_datastore.create_user(username='adminwt0f', password=hashpasswd('adminwt0f'))

    try:
        admin_role = None
        if user_datastore.find_role('Admin'):
            pass
    except Exception as ex:
        admin_role = user_datastore.create_role(name='Admin', description='Admin user role')

    try:
        if user_datastore.find_role('User'):
            pass
    except Exception as ex:
        user_role = user_datastore.create_role(name='User', description='Generic user role')

    if admin and admin_role:
        user_datastore.add_role_to_user(admin, admin_role)
        db.session.commit()


def auth_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = ''
            if request.headers['token']:
                token = request.headers['token']
                decode_token = jwt.decode(token, Config.TOKEN_KEY, algorithm='HS256')
                if (int(time.time()) - decode_token['time']) > Config.EXPIRE_TIME:
                    return jsonify({'code': 5001, 'message': 'Token Expire Time!'})
        except Exception as ex:
            logger.exception(ex.message)
            return jsonify({'code': 5002, 'message': 'Toke is not athorithed or no token!'})
        return func(*args, **kwargs)

    return wrapper


@app.route('/api/login', methods=['post'])
def Login():
    # print 'Headers'
    # for key, value in request.headers.items():
    #     print key, value

    # print request.json['username']
    # for key, value in request.values.items():
    #         print 'keys', key 
    #         print 'values', value, '#' * 20
    # print '=' * 50

    # if request.form.get('username') and request.form.get('password'):
    if request.json['username'] and request.json['password']:
        # username = request.form.get('username')
        username = request.json['username']
        # password = request.form.get('password')
        password = request.json['password']
        user = Users.objects(username=username).first()
        if user is None:
            return jsonify({'code': 4000, 'message': 'Username or password is wrong!'})
        if not user.password == hashpasswd(password):
            return jsonify({'code': 4000, 'message': 'Username or password is wrong!'})

        login_user(user)
        print 'Login successfully', '#' * 100
        time_ = int(time.time())
        token = jwt.encode({'time': time_}, Config.TOKEN_KEY, algorithm='HS256')
        return jsonify({'code': 2000, 'token': token})
    else:

        return jsonify({'code': 6000, 'message': 'Username or password is wrong!'})
        # return make_response(jsonify({'error': 'Username or password is wrong!'}), 400)


@app.route('/api/project/list', methods=['get', 'post'])
@login_required
@auth_token
def ProjectListPage():
    page_num = Config.PAGE_NUMS
    try:
        projects = []
        page = 1
        if request.values.get('page'):
            page = str(request.values.get('page'))
        for project in mongo[Config.MONGODB_C_PROJECTS].find(None, {'_id': 0}):
            projects.append(project)

        # return current page data
        total = len(projects)
        pages = page_num * page
        if total > pages:
            before_page = (page - 1) * page_num
            next_page = page * page_num
            projects = projects[before_page:next_page]
            
        return jsonify({'code': 2000, 'projects': projects, 'total':len(projects)})
    except Exception as ex:
        logger.exception(ex.message)
        return jsonify({'code': 6000, 'message': 'Get project list error!'})


@app.route('/api/project/add', methods=['post'])
@login_required
@auth_token
def ProjectAdd():
    try:
        pid = request.data['pid']
        running_project = mongo[Config.MONGODB_C_PROJECTS].find({'status': 'running'}).count()
        if running_project > Config.MSCAN_RUNNING:
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


@app.route('/api/portinfo', methods=['pid'])
@login_required
@auth_token
def PortInfo():
    try:
        infos = []
        pid = request.data['pid']
        for info in mongo[Config.MONGODB_C_NSCAN].find({'pid': pid}):
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
