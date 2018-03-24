from flask import Flask, request, render_template, jsonify
from twitter_api import twitterClient

app = Flask(__name__)

# Setup the client <query string, retweets_only bool, with_sentiment bool>
api = twitterClient('Trump')

def strtobool(v):
    return v.lower() in ["yes", "true", "t", "1"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tweets')
def tweets():
    retweets_only = request.args.get('retweets_only')
    api.set_retweets_checking(strtobool(retweets_only.lower()))

    with_sentiment = request.args.get('with_sentiment')
    api.set_with_sentiment(strtobool(with_sentiment.lower()))

    query = request.args.get('query')
    api.set_query(query)

    tweets = api.get_tweets()
    return jsonify({'data': tweets, 'count': len(tweets)})

app.run(host="localhost",port=5000,debug=True)