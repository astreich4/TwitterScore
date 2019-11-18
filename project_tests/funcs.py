import requests

def gettime(id):
    #twitter api call
    return id


def getscore(timeline):
    #custom score algo
    ans = timeline
    return ans


def getfact(number):
    #number api call to get fact
    return requests.get('http://numbersapi.com/'+str(number)).text