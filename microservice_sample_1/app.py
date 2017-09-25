import json
from time import sleep
import socket

import requests
from flask import Flask
app = Flask(__name__)

BASE_CONSUL_URL = 'http://consul:8500'
# BASE_CONSUL_URL = 'http://127.0.0.1:8501'

SERVICE_ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 8080

@app.route('/')
def home():
    return 'Hello World from {address}'.format(address=SERVICE_ADDRESS)


@app.route('/health')
def hello_world():
    data = {
        'status': 'healthy'
    }
    return json.dumps(data)

@app.route('/register')
def register():
    url = BASE_CONSUL_URL + '/v1/agent/service/register'
    data = {
        'Name': 'PythonApp',
        'Tags': ['flask'],
        'Address': SERVICE_ADDRESS,
        # 'Address': 'http://127.0.0.0.1:8080',
        'Port': 8080,
        'Check': {
            'http': 'http://{address}:{port}/health'.format(address=SERVICE_ADDRESS, port=PORT),
            # 'http': 'http://127.0.0.1:{port}/health'.format(port=PORT),
            'interval': '10s'
        }
    }
    app.logger.debug('Service registration parameters: ', data)
    res = requests.put(
        url,
        data=json.dumps(data)
    )
    return res.text


if __name__ == '__main__':
    sleep(8)
    try:
        app.logger.debug(register())
    except:
        app.logger.debug('Something wrong happened!')
        pass
    app.run(debug=True, host="0.0.0.0", port=PORT)
