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

# NOTE: flush=True is just for running this script
# with PythonAnywhere's always-on task.
# More info: https://help.pythonanywhere.com/pages/AlwaysOnTasks/
print('this is my twitter bot', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = '/home/selvaprakash/BillD/last_seen_id.txt'



#client = storage.Client()
#bucket = client.get_bucket('billdata')
#blob = bucket.get_blob('remote/path/to/file.txt')

#image_file= arg1

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
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id

        if mentions[0].entities['media'][0]['media_url_https']:
            print('found Image!',mentions[0].entities['media'][0]['media_url_https'], flush=True)
            image = requests.get(mentions[0].entities['media'][0]['media_url_https'], stream=True)
            with open(str(mention.id)+'.png', 'wb') as f:
                shutil.copyfileobj(image.raw, f)
            img_file = { 'file': open(str(mention.id)+'.png','rb')}
            #csv = detect_text_uri(str(mention.id)+'.png')
            url ='https://www.assembill.com/api'
            csv = requests.post(url,files = img_file)
            text_file = open(str(mention.id)+'.txt', "w")
            print (csv.text)
            text_file.write(csv.text)
            text_file.close()
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +' '+
                    csv.text[0:260], mention.id)
            store_last_seen_id(last_seen_id, FILE_NAME)

def sample():
    img_url = 'https://pbs.twimg.com/media/EinO8DTU8AIyLYm.jpg'
    image = requests.get(img_url, stream=True)
    print ('Got Image')
    with open('sample.png', 'wb') as f:
                shutil.copyfileobj(image.raw, f)
    img_file = { 'file': open('sample.png','rb')}
    url ='https://www.assembill.com/api'
    # df_coord = pd.DataFrame(columns=['Field','Position','Start_X','Start_Y','End_X','End_Y'])
    # df_coord = df_coord.append({'Field':'','Start_X':0,'Start_Y':0,'End_X':5000,'End_Y':5000,'Position':1}, ignore_index=True)
    # text_content = img2csv_wip.main_twit_api( df_coord,'sample.png')
    csv = requests.post(url,files = img_file)
    print (csv.text)

while True:
    reply_to_tweets()
    #sample()
    time.sleep(15)