import requests
from requests_oauthlib import OAuth1
import Twitter_key 
import json
from ast import literal_eval
import pandas as pd

def bmp(s):
    return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))

max_pages=50

table = pd.DataFrame({"TWEET_ID":[],"TWEET_TEXT":[],"HASHTAGS":[],"USER_NAME":[],
                      "USER_SCREENNAME":[], "USER_ID":[], "FAVORITE_COUNT":[],
                      "RETWEET_COUNT":[],"USER_LOCATION":[],"DATE":[],
                      "URL_IN_TWEET":[],"USER_MENTIONS":[]})
url ='https://api.twitter.com/1.1/search/tweets.json?q=%23entertainment&lang=en&result_type=mixed&count=100'
count =0
list_id =[]
for i in range(0, max_pages):
    auth = OAuth1(Twitter_key.consumer_key, Twitter_key.consumer_secret,
              Twitter_key.access_token, Twitter_key.access_token_secret)
    
    r = requests.get(url, auth=auth)
    bytes_to_json = r.content.decode('utf-8')
    data = json.loads(bytes_to_json)

    for s in data['statuses']:
        count += 1
        s =str(s).encode('ascii','ignore').decode('utf-8')
        s = bmp(s)
        s = literal_eval(s)
        list_id.append(s['id'])
        table=table.append({"TWEET_ID":s['id'],"TWEET_TEXT":s['text'],
                              "HASHTAGS":[i['text']for i in s['entities']['hashtags']],
                              "USER_NAME":s['user']['name'],
                              "USER_SCREENNAME":s['user']['screen_name'],
                              "USER_ID":s['user']['id'],"FAVORITE_COUNT":s['favorite_count'],
                              "RETWEET_COUNT":s['retweet_count'],"USER_LOCATION":s['user']['location'],
                              "DATE":s['created_at'],"URL_IN_TWEET":[i['url'] for i in s['entities']['urls']],
                              "USER_MENTIONS":s['entities']['user_mentions']},
                             ignore_index=True)
        
    url = url + "&max_id={}".format(min(list_id)-1)


table.to_csv('Informative.csv', mode='a', index=False)
print('**************************')
print('NUMBER_OF_TWEETS: ', count)
 
    

