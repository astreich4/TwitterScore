import requests
import tweepy

import configs

consumer_key = configs.consumer_key1
consumer_secret = configs.consumer_secret1

def gettime(at ,ats):
    #twitter api call
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(at, ats)
    api = tweepy.API(auth)
    timeline = api.user_timeline()
    print(timeline)
    return timeline


def getscore(timeline):
    #custom score algo
    ans = timeline
    return 4


def getfact(number):
    #number api call to get fact
    return requests.get('http://numbersapi.com/'+str(number)).text