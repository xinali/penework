#encoding:utf-8 

import datetime
from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, RoleMixin, UserMixin

db = MongoEngine()

class Roles(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class Users(db.Document, UserMixin):
    username = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Roles), default=[])