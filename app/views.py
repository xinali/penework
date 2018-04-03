#encoding:utf-8 

import os 
import requests
import jwt

from flask_mongoengine import MongoEngine
from flask import Flask, url_for, request, redirect, render_template, \
                  make_response, request, jsonify
from flask_security import Security, MongoEngineUserDatastore, \
                  UserMixin, RoleMixin, login_required,  LoginForm, \
                  url_for_security, current_user, login_user

import pymongo

from models import Users, Roles
from lib.utils.store import hashpasswd
from lib.core.config import Config
from lib.utils.init import initdb
from lib.core.log import logger 

# some init 
# register logger/init db and so on
initdb()

db = MongoEngine()
app = Flask(__name__)
app.config.from_object(Config)

# flask_security config
user_datastore =  MongoEngineUserDatastore(db, Users, Roles)
security = Security(app, user_datastore)

db.init_app(app)

@app.before_first_request
def create_user_role():
    # create admin user
    admin = user_datastore.create_user(username='admintest', password=hashpasswd('admintest'))
    # create User role
    user_role = user_datastore.create_role(name='User', description='Generic user role')
    # create Admin role
    admin_role = user_datastore.create_role(name='Admin', description='Admin user role')
    user_datastore.add_role_to_user(admin, admin_role)
    # db.session.commit()


@app.route('/api/login', methods=['post'])
def Login():
    if request.form.get('username') and request.form.get('password'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.objects(username=username).first()
        if user is None:
            return make_response(jsonify({'error': 'Username or password is wrong!'}), 400)
        if not user.password == hashpasswd(password):
            print user.password, password
            print user.password, hashpasswd(password)
            return make_response(jsonify({'error': 'Username or password is wrong!'}), 400)
        
        login_user(user)
        # token = bcrypt.hashpw(username + '(&*^)' + password)
        token = jwt.encode({'tests':'ttfuc'}, 'nimei', algorithm='HS256')
        return jsonify({'token':token})
    else:
        return make_response(jsonify({'error': 'Username or password is wrong!'}), 400)


@app.route('/api/project/list', methods=['post'])
@login_required
def ProjectList():
    pass 