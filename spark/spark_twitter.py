from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import math
import string
import random
import json

KAFKA_INPUT_TOPIC_NAME_CONS = "tweets"
KAFKA_BOOTSTRAP_SERVERS_CONS = "localhost:9092"

if __name__ == "__main__":
    spark = SparkSession \
    .builder \
    .appName("PySpark Structured Streaming with Kafka") \
    .master("local[*]") \
    .getOrCreate()
    
    print("PySpark Structured Streaming with Kafka Application Started …")
    # Construct a streaming DataFrame that reads from testtopic
    df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS_CONS) \
    .option("subscribe", KAFKA_INPUT_TOPIC_NAME_CONS) \
    .option("startingOffsets", "earliest") \
    .load()
    # df = df.selectExpr("CAST(key AS STRING)","CAST(value AS STRING)", "timestamp").collect()
    
    query = df.writeStream.format("console").start()

    query.awaitTermination()

# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 spark_twitter.py 
