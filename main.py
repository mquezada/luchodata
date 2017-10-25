# -*- coding: utf-8 -*-

import tweepy
import re
from keys import consumer_key, consumer_secret, access_token, access_token_secret
import time
import random

import logging

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s : %(message)s', level=logging.INFO)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.user.screen_name == 'luchodata':
            return

        if "big data" in status.text.lower():
            if status.text.lower().startswith("rt"):
                return

            new_text = status.text
            if new_text.startswith("@"):
                new_text = '.' + new_text

            new_text = re.sub(r'(\bel\b) (big data)', r'\2', new_text, flags=re.IGNORECASE)
            new_text = re.sub(r'(\bal\b) (big data)', r'a \2', new_text, flags=re.IGNORECASE)
            new_text = re.sub(r'(\bdel\b) (big data)', r'de \2', new_text, flags=re.IGNORECASE)
            new_text = re.sub(r'big data', 'Luis Jara', new_text, flags=re.IGNORECASE)
            new_text = re.sub(r'big', 'Luis', new_text, flags=re.IGNORECASE)
            new_text = re.sub(r'data', 'Jara', new_text, flags=re.IGNORECASE)

            logging.info(new_text)
            if len(new_text) <= 140:
                try:
                    if random.random() >= 0.25:
                        api.update_status(new_text)
                    else:
                        logging.info("Last message not triggered")
                except tweepy.TweepError as e:
                    error_code = e.message[0]['code']
                    if error_code == 187:
                        return
                    else:
                        raise e


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(track=['big data'], languages=['es'])

"""
new_text = "A ver, vale que gracias al big data puedan saber que estoy en bancarrota pero ¿seriously?"
new_text = re.sub(r'(\bel\b) (big data)', r'\2', new_text, flags=re.IGNORECASE)
new_text = re.sub(r'(\bal\b) (big data)', r'a \2', new_text, flags=re.IGNORECASE)
new_text = re.sub(r'(\bdel\b) (big data)', r'de \2', new_text, flags=re.IGNORECASE)
new_text = re.sub(r'big data', 'Luis Jara', new_text, flags=re.IGNORECASE)
new_text = re.sub(r'big', 'Luis', new_text, flags=re.IGNORECASE)
new_text = re.sub(r'data', 'Jara', new_text, flags=re.IGNORECASE)
print(new_text)
"""