import praw
import pymongo
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pickle
import json

def sentiment_scores(sentence):
    sentObj = SentimentIntensityAnalyzer()

    sentimentDict = sentObj.polarity_scores(sentence)

    if sentimentDict['compound'] >= 0.05:
        return "Positive"
    elif sentimentDict['compound'] <= -0.05:
        return "Negative"

    return "Neutral"

pickle_in = open("tickersSet.pickle", "rb")
tickers=pickle.load(pickle_in)

credsFile = open('creds.json')
creds = json.load(credsFile)

mongoClient = pymongo.MongoClient(creds["mongoClient"])
tickersDB = mongoClient["TickersTracker"]
tickersCollection = tickersDB["Tickers"]
tickersCollection.drop()

client_id = creds["client_id"]
client_secret = creds["client_secret"]
user_agent = creds["user_agent"]
username = creds["username"]
password = creds["password"]

reddit = praw.Reddit(client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent,
                    username=username,
                    password=password)

wsb = reddit.subreddit("wallstreetbets")
investing = reddit.subreddit("investing")
stocks = reddit.subreddit("stocks")
pennyStocks = reddit.subreddit("pennyStocks")

limit=1000
wsbHot = wsb.hot(limit=limit)
investingHot = investing.hot(limit=limit)
stocksHot = stocks.hot(limit=limit)
pennyStocksHot = pennyStocks.hot(limit=limit)

def loopAndAddPosts(subred):
    for i in subred:
        for phrase in i.title.split():
            if phrase in tickers or phrase.replace('$', '') in tickers:
                phrase = phrase.replace('$', '')
                tickersCollection.update_one({
                    'name': phrase,
                },{
                    '$inc': {
                        'mentions': 1
                }, '$push': {
                    'postInfo': {'postTitle': i.title, 'postLink': i.permalink, 'sentiment': sentiment_scores(i.title)}
                },
                }, upsert=True)            

loopAndAddPosts(wsbHot)
loopAndAddPosts(investingHot)
loopAndAddPosts(stocksHot)
loopAndAddPosts(pennyStocksHot)

if __name__ == 'main':
    pass