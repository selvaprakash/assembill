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
api = tweepy.API(auth, wait_on_rate_limit=True)

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
    print ('last seen id',last_seen_id)
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        # print (mention)
        # break
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        if (mentions[0].user.id == 1304013383591583744):
            last_seen_id = mention.id
            store_last_seen_id(last_seen_id, FILE_NAME)
            break


        if ('media' in mentions[0].entities) and ('copy this' in mention.full_text) and mentions[0]:
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
            op_text = csv.text
            store_last_seen_id(last_seen_id, FILE_NAME)
            continue

        elif 'copy that' in mention.full_text and mentions[0].in_reply_to_status_id :
            parent_tweet_id=mentions[0].in_reply_to_status_id
            print (parent_tweet_id)
            parent_tweet = api.get_status(parent_tweet_id)
            print (type(parent_tweet.entities))
            if  ('media' in parent_tweet.entities):
                print ('Found Image in Parent Tweet')
                image = requests.get(parent_tweet.entities['media'][0]['media_url_https'], stream=True)

                print(parent_tweet.entities['media'][0]['media_url_https'])

                with open(str(parent_tweet.id)+'.png', 'wb') as f:
                    shutil.copyfileobj(image.raw, f)

                img_file = { 'file': open(str(parent_tweet.id)+'.png','rb')}
                url ='https://www.assembill.com/api'
                csv = requests.request("POST",url,files = img_file)
                print (csv.text)
                op_text = csv.text
                if op_text == '':
                    op_text = "Either I didn't find any text or it is in Kiliki which I can't read (yet)"
                    continue
            else:
                op_text = 'No Valid Image Found'
                continue

        else:
            op_text = 'Mention \'@CopyTextApp copy that\' in your reply to the tweet with the image'
            print (op_text)

        print ('Replying to Metion ID:',mention.id)
        print (op_text)
        try:
            api.update_status('@' + mention.user.screen_name +' '+
                op_text[0:279], mention.id)
            print ('Replied')
            last_seen_id = mention.id
        except:
            continue

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