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

BIG_DATA = r'([\'\"]?big data[\'\"]?)'

TRIGGERS = ['emocion', 
            'amor', 
            'music', 
            'spotify', 
            'romance', 
            'pasion',
            'cancion',
            'chile',]


def triggers(text):
    tokens = set(text.lower().split())
    return set(TRIGGERS) & tokens


with codecs.open('luchodata.txt', 'a', encoding='utf-8') as f:
    class MyStreamListener(tweepy.StreamListener):
        def on_status(self, status):
            new_text = status.text
            logging.info(new_text)

            if status.user.screen_name == 'luchodata':
                return

            if "big data" in status.text.lower():
                if status.text.lower().startswith("rt"):
                    return

                if 'marketing' in new_text.lower():
                    return

                if new_text.startswith("@"):
                    new_text = '.' + new_text

                new_text = re.sub(r'&amp;', r'&', new_text)

                new_text = re.sub(r'(\bel\b) ' + BIG_DATA, r'\2', new_text, flags=re.IGNORECASE)
                new_text = re.sub(r'(\bal\b) ' + BIG_DATA, r'a \2', new_text, flags=re.IGNORECASE)
                new_text = re.sub(r'(\bdel\b) ' + BIG_DATA, r'de \2', new_text, flags=re.IGNORECASE)

                new_text = re.sub(r'(\w+)(ar)\b ' + BIG_DATA, r'\1\2 a \3', new_text, flags=re.IGNORECASE)
                new_text = re.sub(r'(\w+)(er)\b ' + BIG_DATA, r'\1\2 a \3', new_text, flags=re.IGNORECASE)
                new_text = re.sub(r'(\w+)(ir)\b ' + BIG_DATA, r'\1\2 a \3', new_text, flags=re.IGNORECASE)

                new_text = re.sub(r'big data', 'Luis Jara', new_text, flags=re.IGNORECASE)
                new_text = re.sub(r'big', 'Luis', new_text, flags=re.IGNORECASE)
                new_text = re.sub(r'data', 'Jara', new_text, flags=re.IGNORECASE)

                new_text = re.sub(r'sociedad', u'televisión', new_text, flags=re.IGNORECASE)

                logging.info(new_text)

                if len(new_text) <= 140:
                    try:
                        if triggers(new_text) or random.random() >= 0.7:
                            api.update_status(new_text)
                            f.write(new_text + '\n')
                        else:
                            logging.info("Last message not triggered")
                    except tweepy.TweepError as e:
                        if e.api_code == 187:
                            return
                        else:
                            raise e
                else:
                    logging.info("Text too long; not triggered")


    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    myStream.filter(track=['big data'], languages=['es'])
