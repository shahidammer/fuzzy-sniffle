# PYSPARK_PYTHON=python spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 spark/spark_twitter.py


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

BROKER_LIST = ",".join(getenv("BROKER_LIST").split(";"))
KAFKA_TOPIC = getenv("KAFKA_TOPIC")

if __name__ == "__main__":

    spark = (
        SparkSession.builder.appName("PySpark Structured Streaming with Kafka")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    print("PySpark Structured Streaming with Kafka Application Started")
    # Construct a streaming DataFrame that reads from testtopic
    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9091")
        .option("subscribe", KAFKA_TOPIC)
        .option("startingOffsets", "earliest")
        .load()
    )
    df = df.selectExpr("CAST(value AS STRING)")
    print(f"Streaming DataFrame : {df.isStreaming}")

    structureSchema = StructType(
        [
            StructField("created_at", StringType(), True),
            StructField("id", StringType(), True),
            StructField("text", StringType(), True),
            StructField(
                "user",
                StructType(
                    [
                        StructField("name", StringType(), True),
                        StructField("id", StringType(), True),
                        StructField("description", StringType(), True),
                        StructField("verfied", BooleanType(), True),
                        StructField("followers_count", IntegerType(), True),
                        StructField("following", IntegerType(), True),
                        StructField("statuses_count", IntegerType(), True),
                        StructField("created_at", StringType(), True),
                        StructField("time_zone", StringType(), True),
                        StructField("profile_image_url", StringType(), True),
                    ]
                ),
            ),
            StructField(
                "retweeted_status",
                StructType(
                    [
                        StructField("id", StringType(), True),
                        StructField("text", StringType(), True),
                        StructField(
                            "user",
                            StructType(
                                [
                                    StructField("name", StringType(), True),
                                    StructField("id", StringType(), True),
                                    StructField("description", StringType(), True),
                                    StructField("verfied", BooleanType(), True),
                                    StructField("followers_count", IntegerType(), True),
                                    StructField("following", IntegerType(), True),
                                    StructField("statuses_count", IntegerType(), True),
                                    StructField("created_at", StringType(), True),
                                    StructField("time_zone", StringType(), True),
                                    StructField(
                                        "profile_image_url", StringType(), True
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
        ]
    )

    tweets = df.select(
        from_json(col("value").cast("string"), structureSchema).alias("tweets")
    ).select("tweets.*")
    tweets.printSchema()

    tweets = (
        tweets.withColumnRenamed("id", "tweet_id")
        .withColumnRenamed("created_at", "tweet_created_at")
        .withColumnRenamed("text", "tweet_text")
    )

    user_df = tweets.select("tweet_id", "tweet_created_at", "tweet_text", "user.*")

    def replace_names(prefix, x):
        if x.startswith("tweet_") or x.startswith("rt_"):
            return x
        return f"{prefix}_{x}"

    new_colnames = list(map(lambda x: replace_names("user", x), user_df.columns))
    user_df = user_df.toDF(*new_colnames)

    rt_df = (
        tweets.select(
            "tweet_id",
            "retweeted_status.id",
            "retweeted_status.text",
            "retweeted_status.user",
        )
        .withColumnRenamed("id", "rt_id")
        .withColumnRenamed("text", "rt_text")
        .select("tweet_id", "rt_id", "rt_text", "user.*")
    )

    new_colnames = list(map(lambda x: replace_names("rt_user", x), rt_df.columns))
    rt_df = rt_df.toDF(*new_colnames)

    final_df = user_df.join(
        rt_df,
        (user_df.tweet_id == rt_df.tweet_id) & (user_df.tweet_id == rt_df.tweet_id),
    )

    final_df.writeStream.outputMode("append").trigger(
        processingTime="60 seconds"
    ).format("csv").option("path", "output/filesink_output").option(
        "header", True
    ).option(
        "checkpointLocation", "checkpoint/filesink_checkpoint"
    ).start().awaitTermination()
