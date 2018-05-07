#encoding:utf-8

from flask_mongoengine import MongoEngine
from flask import Flask
from flask_security import Security, MongoEngineUserDatastore

from models import Users, Roles
from lib.core.config import Config
from lib.utils.store import hashpasswd


VERSION = (0, 1)

__version__ = ".".join(map(str, VERSION))
__status__ = "Alpha"
__description__ = "penework"
__author__ = "xina1i"
__email__ = "daitaomail@gmail.com"


def create_app():

    db = MongoEngine()
    app = Flask(__name__)
    app.config.from_object(Config)
    # flask_security config
    user_datastore = MongoEngineUserDatastore(db, Users, Roles)
    security = Security(app, user_datastore)

    # do some init
    db.init_app(app)
    create_user_role(user_datastore, db)
    return app


def create_user_role(user_datastore, db):
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
