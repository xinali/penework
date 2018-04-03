#encoding:utf-8

import bcrypt
from ..core.config import Config 

def hashpasswd(password):
    if password:
        return bcrypt.hashpw(password.encode('utf-8'), Config.SALT)