# Commands to run 
Start the flask app
```
docker-compose up -d
docker-compose exec mids env FLASK_APP=/w205/project3/game_api.py flask run --host 0.0.0
```
* To do: Add commant to create kafka topic


### Send commands using Apache Bench
Followed example at http://tutorials.jumpstartlab.com/topics/performance/load_testing.html
There are json files with the sample data in the testdata directory

```
docker-compose exec mids ab -n 10 -c 2 -p project3/testdata/steel_sword_user_1.json -T 'application/json' http://localhost:5000/purchase_item/
docker-compose exec mids ab -n 20 -c 2 -p project3/testdata/steel_sword_user_2.json -T 'application/json' http://localhost:5000/purchase_item/
docker-compose exec mids ab -n 5 -c 2 -p project3/testdata/steel_sword_user_2.json -T 'application/json' http://localhost:5000/sell_item/

```

### Read from kafka to ensure that the files are in the queue

```
docker-compose exec mids \
  kafkacat -C -b kafka:29092 -t events -o beginning -e
```

Start spark and connect to Jupyter notebook

```
docker-compose exec spark env PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --port 8888 --ip 0.0.0.0 --allow-root --notebook-dir=/w205/' pyspark
```


Submit spark job from command line

```
docker-compose exec spark spark-submit /w205/project3/process_in_spark.py
```