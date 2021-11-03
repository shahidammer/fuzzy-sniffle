import argparse
from os import getenv
import json
import tweepy

from kafka import KafkaProducer
from kafka.errors import KafkaError

from dotenv import load_dotenv
load_dotenv()

CONSUMER_KEY = getenv('CONSUMER_KEY')
CONSUMER_SECRET = getenv('CONSUMER_SECRET')
ACCESS_TOKEN = getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = getenv('ACCESS_TOKEN_SECRET')
BROKER_LIST = ",".join(getenv('BROKER_LIST').split(";"))
KAFKA_TOPIC = getenv('KAFKA_TOPIC')




producer = KafkaProducer(
    bootstrap_servers=BROKER_LIST,
    value_serializer= lambda m: json.dumps(m).encode('ascii'),
    acks='all',
    compression_type = 'gzip',
    batch_size = 32 * 1024,
    linger_ms = 20,
    )

def on_send_success(msg):
    print(
        f"Topic: {msg.topic} | "
        f"Partition: {msg.partition} | "
        f"Offset: {msg.offset} | ",
        # f"key: {msg.key}"
        )

def on_send_error(excp):
    print(f'I am an errback {excp}')
    # handle exception



class TweetHandler(tweepy.Stream):
    def on_status(self, status):
        _id = str(status._json["id"]).encode()

        with open("backup/backup_tweets.txt", 'a') as f:
            f.write(f"{json.dumps(status._json)}\r\n")
        # p.produce(KAFKA_TOPIC, key=_id, value=json.dumps(status._json),callback=delivery_callback)
        # p.poll(0)

        try:
            producer.send(KAFKA_TOPIC, key=_id, value=json.dumps(status._json)).add_callback(on_send_success).add_errback(on_send_error)
        except KafkaError as e:
            # Decide what to do if produce request failed...
            print(e)
            pass
        # block until all async messages are sent
        # producer.flush(timeout=100)

    def on_error(self, status):
        print("Error detected")


stream = TweetHandler(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
stream.filter(track=["BTC"], threaded=True)
