#!/usr/bin/python3.6

import tweepy
import time
# NOTE: I put my keys in the keys.py to separate them
# from this main file.
# Please refer to keys_format.py to see the format.
from key_format import *
import requests
import shutil
# from img2csv_wip import main_twit_api

print('this is my twitter bot', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

HOME_FOLDER = '/home/selvaprakash/'
TWITS_UPLOAD_FOLDER = HOME_FOLDER+ 'BillD/static/API/copytextapp/'


FILE_NAME = '/home/selvaprakash/BillD/last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    #last_seen_id = 1313035082949521408
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    print ('last seen id',last_seen_id)
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        try:
            parent_tweet_id = mention.in_reply_to_status_id
            print(parent_tweet_id)
            parent_tweet = api.get_status(parent_tweet_id,
                        tweet_mode='extended')
            print (parent_tweet)
            if ('media' in parent_tweet.entities):
                print('Found Image in Parent Tweet')
                image = requests.get(parent_tweet.entities['media'][0]['media_url_https'], stream=True)

                print(parent_tweet.entities['media'][0]['media_url_https'])

                with open(TWITS_UPLOAD_FOLDER+str(parent_tweet.id) + '.png', 'wb') as f:
                    shutil.copyfileobj(image.raw, f)

                img_file = {'file': open(TWITS_UPLOAD_FOLDER+str(parent_tweet.id) + '.png', 'rb')}
                url = 'https://www.assembill.com/twitapi'
                csv = requests.request("POST", url, files=img_file)
                if csv.status_code == 200:
                    op_text = csv.text
                else:
                    print (mention.id, 'POST ERROR')
                    op_text = ''
                print(op_text)
                #op_text = csv.text
                if op_text == '':
                    op_text = "Either We didn't find any text or it is in Kiliki which We can't read (yet)"

                api.update_status('@' + mention.user.screen_name + ' ' +
                                  op_text[0:260], mention.id)
                print('Replied')
                last_seen_id = mention.id

        except  Exception as e:
            print(str(e))
        last_seen_id = mention.id
    store_last_seen_id(last_seen_id, FILE_NAME)

    # print (mention)
def sample():
    img_url = 'https://pbs.twimg.com/media/EinO8DTU8AIyLYm.jpg'
    image = requests.get(img_url, stream=True)
    print ('Got Image')
    with open('sample.png', 'wb') as f:
                shutil.copyfileobj(image.raw, f)
    img_file = { 'file': open('sample.png','rb')}
    url ='https://www.assembill.com/twitapi'

    csv = requests.post(url,files = img_file)
    print (csv.text)

while True:
    reply_to_tweets()
    #sample()
    time.sleep(15)