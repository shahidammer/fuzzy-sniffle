from tweepy import OAuthHandler,Stream
import json

from pykafka import KafkaClient

import sys
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path('../', '.env'))

CONSUMER_KEY = getenv('CONSUMER_KEY')
CONSUMER_SECRET = getenv('CONSUMER_SECRET')
ACCESS_TOKEN = getenv('ACCESS_TOKEN')
ACCESS_SECRET = getenv('ACCESS_SECRET')
BROKER_LIST = ",".join(getenv('BROKER_LIST').split(";"))
KAFKA_TOPIC = getenv('KAFKA_TOPIC')

kafka_client = KafkaClient(BROKER_LIST)
p = kafka_client.topics[bytes(KAFKA_TOPIC,'ascii')].get_producer()

def on_send_success(msg):
	print('yyyy')
def on_send_error(excp):
	print("nnn")
class TweetListener(Stream):
	def on_status(self,status):				
		try:
			tweet=status._json
			print(f"Created at: {tweet['created_at']} Tweet {tweet['id']}")
			text = ",".join(list(tweet.keys()))
			p.produce(bytes(text,'ascii'))
		except Exception as e:
			print(e)
	def on_error(self, status):
		print(status)
		return True

def main():
	query_string = ["BTC","BITCOIN"]
	
	twitter_stream = TweetListener(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_SECRET)
	twitter_stream.filter(languages=['en'], track=query_string)

if __name__ == "__main__":
    main()