#The main code for our App
#two APIs are the twitter API with the tweepy wrapper and the numbersapi
import bcrypt
import pymongo
from flask import Flask, render_template, request, session, redirect, make_response, abort
import tweepy
from requests import Session
import configs
import funcs

#pulling from config file
consumer_key = configs.consumer_key1
consumer_secret = configs.consumer_secret1

#The URL twitter calls back too
callback = 'http://127.0.0.1:5000/oauthhome'

#set up things
app = Flask(__name__)
sess = Session()
app.config.from_object("configs.Config")
app.config['SESSION_TYPE'] = 'filesystem'
client = pymongo.MongoClient("localhost",27017)
db = client.test
users = db.users
scores = db.scores


#the page users hit in the begining prompting them to log on.
@app.route('/')
def index():
    return render_template("front.html")

#Begining of the oauth
@app.route('/auth')
def auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(url)

#where twitter sends you back too
@app.route('/oauthhome')
def twitter_callback():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)

    #gets the access tokens after twitter
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

    #gets the twitter username
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(at, ats)
    api = tweepy.API(auth)
    user = api.me()
    screenname = user.screen_name

    #saves the username, access token secret, the hashed access token secret into collection users in the DB
    salt =bcrypt.gensalt()
    hashed = bcrypt.hashpw(ats.encode('utf8'),salt)
    hashed = hashed.decode()
    users.insert({"screen_name": screenname, "access_token": at, "access_token_secret": ats, "atshash": hashed, "salt": salt})
    resp = make_response(redirect('/home'))
    resp.set_cookie('id', value=hashed, httponly=True)
    return resp

#the logged on home page
@app.route('/home')
def home():
    if 'id' in request.cookies:
        #check if its the same
        test = request.cookies.get('id')
        comp = db.users.find_one({"atshash": test})

        #print statements for debugging
        #print(test)
        #print(comp["atshash"])
        #print(comp)
        if test == comp["atshash"]:
            #you only get to here if you have a cookie that matches one in the DB
            resp = make_response(render_template("home.html",uname=comp["screen_name"]))
            # builds the cookie to maintain logged on user
            resp.set_cookie('id', value=test, httponly=True)
        else:
            #print("error 1")
            abort(401)
    else:
        #print("error2")
        abort(401)
    return resp

#the page that contains the score
@app.route('/score', methods=['POST','GET'])
def score():
    if 'id' in request.cookies:
        #check if its the same
        test = request.cookies.get('id')
        comp = db.users.find_one({"atshash": test})
        #prints for debugging
        #print(test)
        #print(comp["atshash"])
        #print(comp)
        if test == comp["atshash"]:

            at = comp["access_token"]
            ats = comp["access_token_secret"]

            #The block for calling all the functins to build the score and fact
            timeline = funcs.gettime(at, ats)
            number = funcs.getscore(timeline)
            ans = funcs.getfact(number)

            #This is alll the stuff to update to and add each user with their score to a db for
            #the leaderboard.
            #currently not implemented
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(at, ats)
            api = tweepy.API(auth)
            user = api.me()
            screenname = user.screen_name
            finduser = db.scores.find_one({"screen_name":screenname})
            if finduser is not None:
                userid = finduser["_id"]
                db.scores.update({"_id": userid}, { "$set":{"score": number}})
            else:
                scores.insert({"screen_name": screenname, "score": number})

            #making the respone ie: the weppage to be sent back with the correct values
            resp = make_response(render_template('score.html', fact=ans, scr=number))
            #builds the cookie to maintain logged on user
            resp.set_cookie('id', value=test, httponly=True)
        else:
            #print("error 1")
            abort(401)
    else:
        #print("error2")
        abort(401)
    return resp

#the logout request, redirects a user to the / page
@app.route("/logout")
def logout():
    if 'id' in request.cookies:
        #check if its the same
        test = request.cookies.get('id')
        comp = db.users.find_one({"atshash": test})
        #comp = comp["atshash"]

        if test == comp["atshash"]:
            #prints for debugging
            #print(test)
            #print(comp["atshash"])
            #print(comp)

            #removes the user from the DB
            users.remove(comp)
            #builds the response but doesnt add the cookie
            resp = make_response(redirect('/'))

        else:
            #print("error 1")
            abort(401)
    else:
        #print("error2")
        abort(401)
    return resp


if __name__ == '__main__':
    sess.init_app(app)
    app.run(debug=True)


