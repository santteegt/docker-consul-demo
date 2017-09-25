import json
from time import sleep
import socket

import requests
from flask import Flask, abort
app = Flask(__name__)

BASE_CONSUL_URL = 'http://consul:8500'
# BASE_CONSUL_URL = 'http://127.0.0.1:8501'
SAMPLE_QUERY_FILE = 'consul.query.sample.json'

PORT = 8080
MICROSERVICE_ID = None

@app.route('/')
def home():
    return 'Hello World!'


@app.route('/call/service/1')
def connect_microservice_1():
    
    MICROSERVICE_ID = register_query()
    print('Micoservice ID: ', MICROSERVICE_ID)

    url = BASE_CONSUL_URL + '/v1/query/' + MICROSERVICE_ID + '/execute'
    rs = requests.get(url)
    if rs.ok:

        json_rs = rs.json()
        print(json_rs)

        datacenter = json_rs['Datacenter']
        nodes = json_rs['Nodes']
        for node in nodes:
            service = node['Service']
            address = service['Address']
            port = service['Port']

            url = 'http://{address}:{port}'.format(address=address, port=port)
            rs = requests.get(url)
            response = 'Response from microservice {service} located in datacenter {datacenter}: \n\n <strong>{response}</strong>' \
                .format(service=service, datacenter=datacenter, response=rs.text) \
                if rs.ok else 'Problem trying to call {service}'.format(service=service)
            
            return response
    else:
        print('ERROR WHILE TRYING TO DISCOVER MICROSERVICE WITH ID ', MICROSERVICE_ID)

    return rs.text


@app.route('/health')
def hello_world():
    data = {
        'status': 'healthy'
    }
    return json.dumps(data)


def register_query():
    url = BASE_CONSUL_URL + '/v1/query'


    json_query = json.load(open(SAMPLE_QUERY_FILE, 'r'))

    rs = requests.post(url, data=json.dumps(json_query))
    if rs.ok:
        json_rs = rs.json()
        microservice_id = json_rs['ID']
        return microservice_id
    else:
        return get_query_id()

def get_query_id():

    url = BASE_CONSUL_URL + '/v1/query'

    rs = requests.get(url)
    if rs.ok:
        json_rs = rs.json()
        print(json_rs)
        for query in json_rs:
            if query['Name'] == 'sample-query':
                microservice_id = query['ID']
                return microservice_id
                break
    else:
        print('CONSUL IS NOT AVAILABLE')
        abort(503)


if __name__ == '__main__':
    sleep(8) # Waiting to Consul to complete startup 

    app.run(debug=True, host="0.0.0.0", port=PORT)
