#encoding:utf-8 

# from os import sys, path
# sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from views import app
from lib.utils.init import initdb

# do some init
initdb()

# if __name__ == "__main__":
    # initdb()
    # app.run(host='0.0.0.0', debug=True, port=8080)
