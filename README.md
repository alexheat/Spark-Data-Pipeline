

# Commands to run 

#### Open terminal window 1 to start start the containers, create kafka topic, and start flask app 
```
cd w205/project3/

docker-compose up -d

docker-compose exec kafka kafka-topics --create --topic events --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181

docker-compose exec kafka kafka-topics --list --zookeeper zookeeper:32181

docker-compose exec mids env FLASK_APP=/w205/project3/game_api.py flask run --host 0.0.0.0

```


#### Open terminal window 2 to tail the kafka logs.
```
cd w205/project3/

docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning
```

#### Open terminal window 3 to run script to create random events
Run bash script to create random events using apache bench jobs again and see it logged in windows 3
```
chmod +x runner.sh
bash runner.sh
```

#### Open terminal window 4 for running spark commands
Submit spark job from command line

```
cd w205/project3/

docker-compose exec spark spark-submit /w205/project3/process_in_spark.py
```


#### Open terminal window 5 for running hive and presto
Check the files written to hadoop 

```
cd w205/project3/

docker-compose exec cloudera hadoop fs -ls /tmp/game

```
Create tables that can be queried in presto<br>
Create table called purchase API 

```
docker-compose exec cloudera hive

create external table if not exists default.purchase_api (
    currency string,
    event_type string,
    item string,
    item_type string,
    price double,
    timestamp string,
    user_id string
  )
  stored as parquet 
  location '/tmp/game/purchase_api'
  tblproperties ("parquet.compress"="SNAPPY");
  
  
  
create external table if not exists default.sell_api (
    game_api_raw string,
    timestamp string,
    event_type string,
    item string,
    item_type string,
    user_id string,
    price double,
    currency string
  )
  stored as parquet 
  location '/tmp/game/sell_api'
  tblproperties ("parquet.compress"="SNAPPY");

create external table if not exists default.purchase_api (
    game_api_raw string,
    timestamp string,
    event_type string,
    item string,
    item_type string,
    user_id string,
    price double,
    currency string
  )
  stored as parquet 
  location '/tmp/game/purchase_api'
  tblproperties ("parquet.compress"="SNAPPY");
  
``` 
Type `ctrl+d` to exit hive 

#### Query presto in in window 5

```
docker-compose exec presto presto --server presto:8080 --catalog hive --schema default
show tables;

select count(*) as Count from purchase_api;
select count(*) as Count from sell_api;
select * from purchase_api limit 5;
select * from sell_api limit 5;
select user_id, sum(price) as Revenue from purchase_api group by user_id;
select item, count(*) as ItemsSold from sell_api group by item;
```
