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
    return timeline


def getscore(timeline):
    #custom score algo, currently just a sum of your most recent favorites
    print(len(timeline))
    numtweets = len(timeline)
    temp = timeline[0]._json
    count = 0
    favcount = 0
    while count < numtweets:
        temptweet = timeline[count]._json
        favcount += temptweet["favorite_count"]
        count += 1
    return favcount


def getfact(number):
    #number api call to get fact
    return requests.get('http://numbersapi.com/'+str(number)).text