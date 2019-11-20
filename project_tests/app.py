import datetime
import bcrypt
import pymongo
import json
from flask import Flask, render_template, request, session, redirect, make_response, abort
import tweepy
from requests import Session
import configs
import funcs

consumer_key = configs.consumer_key1
consumer_secret = configs.consumer_secret1

callback = 'http://127.0.0.1:5000/oauthhome'

app = Flask(__name__)
sess = Session()
app.config.from_object("configs.Config")
app.config['SESSION_TYPE'] = 'filesystem'
client = pymongo.MongoClient("localhost",27017)
db = client.test
users = db.users
sysinfo = db.sysinfo



@app.route('/')
def index():
    #post = {"author": "Mike","text": "My first blog post!","tags": ["mongodb", "python", "pymongo"],}
    #users.insert({"name":"helloworlds"})
    return render_template("front.html")

@app.route('/auth')
def auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(url)


@app.route('/oauthhome')
def twitter_callback():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)

    verifier = request.args.get('oauth_verifier')
    token = request.args.get('oauth_token')
    auth.request_token = {'oauth_token': token,
                          'oauth_token_secret': verifier}
    print("test1", auth.request_token)
    #must run auth.get_access_token
    print("test2", auth.get_access_token(verifier))
    at = auth.access_token
    ats = auth.access_token_secret
    sessio = (at, ats)
    print("callback2", sessio)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(at, ats)
    api = tweepy.API(auth)
    user = api.me()
    screenname = user.screen_name

    salt =bcrypt.gensalt()
    hashed = bcrypt.hashpw(ats.encode('utf8'),salt)
    hashed = hashed.decode()
    users.insert({"screen_name": screenname, "access_token": at, "access_token_secret": ats, "atshash": hashed, "salt": salt})
    resp = make_response(redirect('/home'))
    resp.set_cookie('id', value=hashed, httponly=True)
    return resp

@app.route('/home')
def home():
    if 'id' in request.cookies:
        #check if its the same
        test = request.cookies.get('id')
        comp = db.users.find_one({"atshash": test})
        comp = comp["atshash"]
        print(test)
        print(comp)
        if test == comp:
            resp = make_response("user logged on")
        else:
            #print("error 1")
            abort(401)
    else:
        print("error2")
        abort(401)
    return resp

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


