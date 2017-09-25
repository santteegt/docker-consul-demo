
# Service Discovery using Consul

The aim of this repository is to present an hands-on tutorial on how to setup Consul as a service discovery framework. One of main advantages of Consul are its available REST API to register and query services, so it is not necessary to import extra libraries and/or dependencies to manage the communication between services.

## Installation instructions

1. Requirements

* Docker 3.2+

2. Run the following commands:

```
$ git clone <REPO_GIT_URL>
$ cd docker-consul-demo
$ docker-compose up  
```


## How to check everything is working ?

* The sample microservice implements AS A MUST the [health method](http://127.0.0.1:8080/health) to allow Consul to check the service status.
* Access the leader node WebUI [http://localhost:8501/ui/](http://127.0.0.1:8501/ui/) and check services status. You can also have access using one of the replicas Web UI as well. In this example: `consul_replica` node access to the WebUI is through `port 8502`
* Get available services through API: [http://127.0.0.1:8501/v1/agent/services](http://127.0.0.1:8501/v1/agent/services)
* To test the communication between microservices using Consul by accesing the following link [http://127.0.0.1:8180/call/service/1](http://127.0.0.1:8180/call/service/1)


## Create and execute service queries

* To create a sample query template, run the following command:

```
$ curl --request POST --data @consul.query.sample.json http://127.0.0.1:8501/v1/query >> query_id.json
```

In this tutorial, the query registration is made through the [Microservice Sample 2](microservice_sample_2/Server.py)

* To Executing the prepared service query created above, copy the ID field from `query_id.json` file and run the following command:

```
$ curl --request GET http://127.0.0.1:8501/v1/query/<query-template-id>/execute
```

An example of query response can be seen in [query_execution.sample.json](query_execution.sample.json) file.

* To query current available queries:

```
$ curl --request GET http://127.0.0.1:8501/v1/query
```
