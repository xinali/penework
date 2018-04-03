from flask import Flask, jsonify, abort

app = Flask(__name__)
from lib.core.log import logger

def main():
    try:
        a = 0
        b = 3
        print b / a
    except Exception as ex:
        logger.exception()
    

if __name__ == '__main__':
    main()