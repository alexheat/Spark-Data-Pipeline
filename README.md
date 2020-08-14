
# Project 3: Understanding User Behavior
*Jude Kavalam, Alex Heaton*

## Files included:
 - README.md: Project overview and commands used to create pipeline and query data. 
 - game_api.py: Code for flask API that logs events to kafka.
 - process_in_spark.py: Code to process streaming events from Kafka and store to parquet files in HDFS.
 - runner.sh: Bash script to continuously generate sample data by calling the APIs using Apache Bench. 
 - docker-compose.yml: Docker compose file with images and configuration required for the pipeline. 

## Project notes:
- The project has two apis: purchase and sell. Purchase is a user buying an item from the game developer and sell is a user selling the item back to the game developer or another user. 
- We have implimented a POST method in our API that can accept additional properties about each transaction. The schema of the properties that we collect through these APIs are:

```
user_id: string ["5"]
price:double [5]
currency:string ["USD"]
item:string ["Steel Shield"]
item_type:string ["Shield"]
timestamp:datetime ["2020-08-04 14:09:59.73"]
event_type:string ["purchase_api"]
```
- A bash script (runner.sh) will continously call the API and generate random values for price, user_id, item, and randomly alternate which API is called (sell or purchase). 

## Commands to run: 


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
cd w205/project3/
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
```
**Query 1:** Show the total transactions and most recent transactions from each table.
```
select event_type, count(*) as Transactions, sum(price) as Revenue, max(timestamp) as LastTransactionTime from purchase_api group by event_type
UNION
select event_type, count(*) as Transactions, sum(price) as Revenue, max(timestamp) as LastTransactionTime from sell_api group by event_type;
```
Sample output from query 1

event_type   | Transactions | Revenue |       LastTransactionTime        
---------------|--------------|---------|-------------------------
 purchase_item |          278 |  4116.0 | 2020-08-04 14:02:04.508 
 sell_item     |          292 |  4328.0 | 2020-08-04 14:02:09.705 

The bash script is still running in the background so running the same query again will return different results

Sample output from query 1 after several minutes 

  event_type   | Transactions | Revenue |       LastTransactionTime        
---------------|--------------|---------|-------------------------
 purchase_item |          426 |  6286.0 | 2020-08-04 14:09:54.528 
 sell_item     |          502 |  7458.0 | 2020-08-04 14:09:59.73  


**Query 2:** What are the most popular items (in terms of purchases) ranked by total revenue. 

```
select item, item_type, sum(price) as Revenue, count(*) as Transactions, avg(price) as AverageSellingPrice from purchase_api 
group by item, item_type order by Revenue desc;
```
Sample output from query 2


 item     | item_type | Revenue | Transactions | AverageSellingPrice 
--------------|-----------|---------|--------------|---------------------
 Steel Sword  | Sword     |  6350.0 |          416 |  15.264423076923077 
 Steel Shield | Shield    |  6056.0 |          396 |  15.292929292929292


**Query 3:** Which users are selling the most items. 

```
select user_id, sum(price) as Revenue, count(*) as Transactions from sell_api
group by user_id order by Transactions desc;
```
Sample output from query 3

 user_id | Revenue | Transactions 
---------|---------|--------------
 1       |  3924.0 |          234 
 5       |  3334.0 |          228 
 3       |  3376.0 |          220 
 4       |  2970.0 |          204 
 2       |  2830.0 |          188 