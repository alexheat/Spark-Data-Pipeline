

- Expose Flask app to the Internet by creating a new firewall with the following settings:
    - IP ranges: 0.0.0.0/0
    - tcp:5000

# Commands to run 

Start the flask app

```
docker-compose exec mids env FLASK_APP=/w205/project3/game_api.py flask run --host 0.0.0
```

Call the API. I use post man. Sample call:

```
POST http://35.185.212.192:5000/purchase_a_sword
Request Headers
    User-Agent: PostmanRuntime/7.26.1
    Accept: */*
    Cache-Control: no-cache
    Postman-Token: 18b958ec-8edd-420c-971f-a756782ae314
    Host: 35.185.212.192:5000
    Accept-Encoding: gzip, deflate, br
    Connection: keep-alive
Request Body
    price: "99.99"
    currency: "USD"
    user_id: "abc123↵"
```
Retun response

```
{'event_type': 'purchase_sword', 'request_headers': {'Accept-Encoding': u'gzip, deflate, br', 'Host':
u'35.185.212.192:5000', 'Accept': u'*/*', 'User-Agent': u'PostmanRuntime/7.26.1', 'Connection': u'keep-alive',
'Referer': u'http://35.185.212.192:5000/purchase_a_sword', 'Cache-Control': u'no-cache', 'Postman-Token':
u'f3508413-dadc-4c12-b50d-96410ba50cbb'}}Sword Purchased!
```

## Read from kafka

```
docker-compose exec mids \
  kafkacat -C -b kafka:29092 -t events -o beginning -e
```

Start spark and connect to Jupyter notebook


```
docker-compose exec spark env PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --port 8888 --ip 0.0.0.0 --allow-root --notebook-dir=/w205/' pyspark
```