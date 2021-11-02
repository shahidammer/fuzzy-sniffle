from tweepy import OAuthHandler,Stream
import tweepy,json

from pykafka import KafkaClient

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path('../', '.env'))

class TweetListener(tweepy.StreamListener):
	def __init__(self,api=None):
		super(TweetListener,self).__init__()
		self.client = KafkaClient("127.0.0.1:9092")
		self.producer = self.client.topics[bytes('twitter','ascii')].get_producer()
	def on_status(self,status):		
		try:
			tweet=status._json
			self.producer.produce(bytes(json.dumps(tweet),'ascii'))
		except Exception as e:
			print(e)
	def on_error(self, status):
		print(status)
		return True

def main():
	query_string = ["BTC","BITCOIN"]
	
	CONSUMER_KEY = os.getenv('CONSUMER_KEY')
	CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
	ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
	ACCESS_SECRET = os.getenv('ACCESS_SECRET')

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	l = TweetListener()
	twitter_stream = tweepy.Stream(auth, l)
	twitter_stream.filter(languages=['en'], track=query_string)

if __name__ == "__main__":
    main()