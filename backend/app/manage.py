#encoding:utf-8 

from views import app
from lib.utils.init import initdb


if __name__ == "__main__":
    initdb()
    app.run(host='0.0.0.0', debug=True, port=8070)
