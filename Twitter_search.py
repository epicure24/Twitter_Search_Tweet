import requests
from requests_oauthlib import OAuth1
import Twitter_key 
import json
from ast import literal_eval
import pandas as pd

def bmp(s):
    return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))

max_pages=100

url ='https://api.twitter.com/1.1/search/tweets.json?q=%23food&lang=en&result_type=mixed&count=100'
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
        print("**********************TWEET NUMBER************************ :",count)
        print()
        print(s['text']) #for the tweet text ..if you want all info just print(s)
        print()
        print("**********************Next_Tweet*************************")

        
    url = url + "&max_id={}".format(min(list_id)-1)


print()
print('NUMBER_OF_TWEETS: ', count)
 
    

