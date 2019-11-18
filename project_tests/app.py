from flask import Flask, render_template, request, make_response, session, redirect, g
import requests
import tweepy
from requests import Session
import configs
import funcs


consumer_key = configs.consumer_key1
consumer_secret = configs.consumer_secret1

callback = 'http://127.0.0.1:5000/oauthhome'

app = Flask(__name__)

global sess
sess = Session()

app.config.from_object("configs.Config")



@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        pass
    else:
        return render_template('index.html')


@app.route('/auth', methods=['POST','GET'])
def auth():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token['oauth_token']
    print("auth",session)
    print(url)
    url = redirect(url)
    print(url)
    return url


@app.route('/oauthhome', methods=['POST','GET'])
def twitter_callback():
    """
print("callback",session)
    token = session.get('request_token')
    print(token)
"""



    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)

    verifier = request.args.get('oauth_verifier')
    token = request.args.get('oauth_token')
    auth.request_token = {'oauth_token': token,
                          'oauth_token_secret': verifier}
    print(auth.request_token)
    sessio = (auth.access_token, auth.access_token_secret)
    print("callback2",sessio)

    return redirect('/app')

@app.route('/app', methods=['POST','GET'])
def request_twitter():
    print(session)
    token, token_secret = session['token']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    return api.me()

@app.route('/score', methods=['POST','GET'])
def score():
    id = request.form['Username']
    timeline = funcs.gettime(id)
    number = funcs.getscore(timeline)
    ans = funcs.getfact(number)
    return render_template('score.html', fact=ans, scr=number)


if __name__ == '__main__':
    sess.init_app(app)
    app.run(debug=True)


