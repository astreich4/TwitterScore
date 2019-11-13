from flask import Flask, render_template, request, make_response
import requests


app = Flask(__name__)


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
