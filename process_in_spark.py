#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import udf
from pyspark import SparkContext
import sys

sc =SparkContext()

def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .getOrCreate()
    
    #Read events from kafka
    game_api_raw = spark \
      .read \
      .format("kafka") \
      .option("kafka.bootstrap.servers", "kafka:29092") \
      .option("subscribe","events") \
      .option("startingOffsets", "earliest") \
      .option("endingOffsets", "latest") \
      .load() 
    game_api_raw.cache()

    #Select the 'value' collumn as a string so it can be converted to a json object 
    game_api_string = game_api_raw.select(game_api_raw.value.cast('string'))
    game_api_df = game_api_string.rdd.map(lambda x: json.loads(x.value)).toDF()

    #Save all of the responses with all collumns to a parque file
    game_api_df.write.mode("overwrite").parquet("/tmp/game/all_api_requests")

    #Drop the collum with the request headers as they are not need for the downstream analysis 
    game_api_df_light = game_api_df.drop('request_headers')
    game_api_df_light.show()

    #Save the purchases and sales to seperate files for analysis 
    game_api_df_light.filter(game_api_df_light.event_type=="sell_item").write.mode("overwrite").parquet("/tmp/game/sell_api")
    game_api_df_light.filter(game_api_df_light.event_type=="purchase_item").write.mode("overwrite").parquet("/tmp/game/purchase_api")

    
    #Create a function that can be used to list the contents of a directory in Hadoop

    def list_hadoop_files(path):
        hadoop = sc._jvm.org.apache.hadoop
        fs = hadoop.fs.FileSystem
        conf = hadoop.conf.Configuration() 
        fs_path = hadoop.fs.Path(path)

        try:
            for f in fs.get(conf).listStatus(fs_path):
                print(f.getPath(), f.getLen())
        except:
            print("Path '{}' does not exist.".format(path))

    #Check that the files were created in Hadoop
    print('\n++++++++++\n SHOW PARQUET FILES THAT WERE CREATED \n')
    list_hadoop_files('/tmp/game/')
    print('\n++++++++++\n')

if __name__ == "__main__":
    main()