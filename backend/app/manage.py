#encoding:utf-8 

from views import app
from lib.utils.init import initdb

# do some init
initdb()

# if __name__ == "__main__":
    # initdb()
    # app.run(host='0.0.0.0', debug=True, port=8082)
