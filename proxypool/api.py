from flask import Flask
from proxypool.db import RedisClient
from proxypool.settings import *


app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>免费代理池</h2>'


@app.route('/fetch')
def fetch():
    client = RedisClient()
    if client.random() is None:
        return '代理池为空'
    return client.random()


@app.route('/count')
def count():
    client = RedisClient()
    print('总数：', client.count())
    return str(client.count())


def start_api(host=API_HOST, port=API_PORT):
    app.run(host=host, port=port)


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)
