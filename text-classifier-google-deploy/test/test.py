from urllib import response
import requests
import json

## Creates a new entry in the catalog
new_tweet = {'tweet':'black queen is the best survive in the world and nobody cannot tell the contrary'}


#end_point = "host/tweet/new"
response = requests.post(end_point,json=new_tweet)


tweet_class = json.loads(response.text)
print(tweet_class['label'])