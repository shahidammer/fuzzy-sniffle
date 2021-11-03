from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import math
import string
import random
import json
from os import getenv

from pathlib import Path
from dotenv import load_dotenv

# load_dotenv(dotenv_path=Path('../', '.env'))
load_dotenv()

BROKER_LIST = ",".join(getenv('BROKER_LIST').split(";"))
KAFKA_TOPIC = getenv('KAFKA_TOPIC')

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
        .option("kafka.bootstrap.servers", "localhost:9091") \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "earliest") \
        .load()

    tweet_schema = StructType([
        StructField("created_at", StringType(), True),
        StructField("id", StringType(), True),
        StructField("text", StringType(), True),
        ])



    df = df.selectExpr("CAST(value AS STRING)")

    tweets = df.select(from_json(col("value").cast("string"), tweet_schema).alias("tweets")).select("tweets.*")
    tweets.printSchema()

    query = tweets.writeStream.outputMode("append").format("console").start()
    query.awaitTermination()


    # query2 = tweets.writeStream.format("console").start()
    # query2.awaitTermination()

    # structureSchema = StructType([
    #     StructField('name', StructType([
    #          StructField('firstname', StringType(), True),
    #          StructField('middlename', StringType(), True),
    #          StructField('lastname', StringType(), True)
    #          ])),
    #      StructField('id', StringType(), True),
    #      StructField('gender', StringType(), True),
    #      StructField('salary', IntegerType(), True)
    #      ])



# PYSPARK_PYTHON=python spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 spark_twitter.py 
