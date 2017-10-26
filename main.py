# -*- coding: utf-8 -*-

import tweepy
import re
from keys import consumer_key, consumer_secret, access_token, access_token_secret
import codecs
import random

import logging

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s : %(message)s', level=logging.INFO)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


with codecs.open('luchodata.txt', 'a', encoding='utf-8') as f:
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

                new_text = re.sub(r'(\w+)(ar)\b (big data)', r'\1\2 a \3', new_text, flags=re.IGNORECASE)
                new_text = re.sub(r'(\w+)(er)\b (big data)', r'\1\2 a \3', new_text, flags=re.IGNORECASE)
                new_text = re.sub(r'(\w+)(ir)\b (big data)', r'\1\2 a \3', new_text, flags=re.IGNORECASE)

                new_text = re.sub(r'big data', 'Luis Jara', new_text, flags=re.IGNORECASE)
                new_text = re.sub(r'big', 'Luis', new_text, flags=re.IGNORECASE)
                new_text = re.sub(r'data', 'Jara', new_text, flags=re.IGNORECASE)

                logging.info(new_text)
                if len(new_text) <= 140:
                    try:
                        if random.random() >= 0.25:
                            api.update_status(new_text)
                            f.write(new_text + '\n')
                        else:
                            logging.info("Last message not triggered")
                    except tweepy.TweepError as e:
                        if e.api_code == 187:
                            return
                        else:
                            raise e


    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    myStream.filter(track=['big data'], languages=['es'])
