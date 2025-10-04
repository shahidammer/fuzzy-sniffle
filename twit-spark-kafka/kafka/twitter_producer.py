from tweepy import OAuthHandler, Stream
import json

from kafka import KafkaProducer
from kafka.errors import KafkaError
import time
import sys
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

# load_dotenv(dotenv_path=Path('../', '.env'))
load_dotenv()

CONSUMER_KEY = getenv("CONSUMER_KEY")
CONSUMER_SECRET = getenv("CONSUMER_SECRET")
ACCESS_TOKEN = getenv("ACCESS_TOKEN")
ACCESS_SECRET = getenv("ACCESS_SECRET")
BROKER_LIST = ",".join(getenv("BROKER_LIST").split(";"))
KAFKA_TOPIC = getenv("KAFKA_TOPIC")


p = KafkaProducer(
    bootstrap_servers=BROKER_LIST,
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
    acks="all",
    # compression_type = 'gzip',
    batch_size=32 * 1024,
    linger_ms=20,
)


def on_send_success(msg):
    print(
        f"{msg.timestamp} | Topic: {msg.topic} | "
        f"Partition: {msg.partition} | "
        f"Offset: {msg.offset} | "
    )


def on_send_error(excp):
    print(f"I am an errback {excp}")
    # handle exception


class TweetListener(Stream):
    def on_status(self, status):
        try:
            tweet = status._json
            p.send(
                KAFKA_TOPIC, key=str(tweet["id"]).encode("ascii"), value=tweet
            ).add_callback(on_send_success).add_errback(on_send_error)
        except Exception as e:
            print(e)
        time.sleep(1)
        # p.flush(timeout=100)

    def on_error(self, status):
        print(status)
        return True


def main():
    query_string = ["BTC", "BITCOIN"]

    twitter_stream = TweetListener(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
    )
    twitter_stream.filter(languages=["en"], track=query_string)


if __name__ == "__main__":
    main()
