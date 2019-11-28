from flask import Flask, render_template, request, make_response
import requests


app = Flask(__name__)
consumer_key = ''
consumer_secret = ''
callback = 'http://yourdoamain.com/callback'

@app.route('/auth')
def auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(url)

@app.route('/callback')
def twitter_callback():
    request_token = session['request_token']
    del session['request_token']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)
    session['token'] = (auth.access_token, auth.access_token_secret)

    return redirect('/app')

@app.route('/app')
def request_twitter:
    token, token_secret = session['token']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    return api.me()

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        pass
    else:
        return render_template('index.html')


@app.route('/score', methods=['POST','GET'])
def score():
    id = request.form['Username']
    timeline = gettime(id)
    number = getscore(timeline)
    ans = getfact(number)
    return render_template('score.html', fact=ans,scr = number)


if __name__ == '__main__':
    app.run(debug=True)


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
