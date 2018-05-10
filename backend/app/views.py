# encoding:utf-8

import jwt
import time
from functools import wraps

from flask import request, redirect, request, jsonify
from flask_security import  login_required, login_user

from models import Users, Roles
from lib.utils.store import hashpasswd
from lib.core.config import Config
from lib.core.log import logger
from lib.core.db import mongo
from app import create_app

app = create_app()

from celery import Celery
from celery.result import AsyncResult
def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
celery = make_celery(app)

@celery.task()
def scan(pid, scan_ip_range, scan_ports, scan_rate): 

    from utils.masscan import MScan
    from utils.nscan import nscan

    mscan = MScan()
    mscan.run()
    nscan()

    return 'Done'


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
            page = int(request.values.get('page'))

        for project in mongo[Config.MONGODB_C_PROJECTS].find(None, {'_id': 0}):
            projects.append(project)

        # return current page data
        total = len(projects)
        pages = page_num * page
        print 'pages', pages, '#' * 200
        if total > pages:
            before_page = (page - 1) * page_num
            next_page = page * page_num
            projects = projects[before_page:next_page]
        
        # update project status
        for project in projects:
            pid = project['pid']
            status = AsyncResult(int(pid)).state
            mongo[Config.MONGODB_C_PROJECTS].update_one({'pid':pid}, \
                                    {'$set': {'status': status}}, upsert=False)

        return jsonify({'code': 2000, 'projects': projects, 'total':len(projects)})
    except Exception as ex:
        logger.exception(ex.message)
        return jsonify({'code': 6000, 'message': 'Get project list error!'})


@app.route('/api/project/add', methods=['post'])
@login_required
@auth_token
def ProjectAdd():
    try:
        # check pid exists
        if request.json['pid']:
            pid = request.json['pid']
            # pid exists in backend or not
            if  mongo[Config.MONGODB_C_PROJECTS].find({'pid': pid}):
                return jsonify({'code': 4000, 'message': 'Project exists!'})

        if  request.json['domain'] and request.json['scan_ports'] \
            and request.json['scan_ip_range'] and request.json['pid']:

            # nesscery data
            pid = request.json['pid']
            domain = request.json['domain']
            scan_ports = request.json['scan_ports']
            scan_ip_range = request.json['scan_ip_range']
            project_name = request.json['project_name']
            description = request.json['description']
            scan_requency  = request.json['scan_requency']
            scan_rate = request.json['scan_rate']

            job = scan.apply_async(pid, scan_ip_range, scan_ports, scan_rate, task_id=int(pid))
            status = job.state
            mongo[Config.MONGODB_C_PROJECTS].insert({'pid'pid, 
                                                     'domain':domain, 
                                                     'project_name':project_name, 
                                                     'description': description,
                                                     'status': status
                                                    })
            return jsonify({'codd': 2000, 'message': 'Add project successfully'})
        else:
            return jsonify({'code': 4000, 'message': 'No pid Specify'})
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
