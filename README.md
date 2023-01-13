# Reddit Stocks Scraper

This is a scraper that will find the last most top mentioned stocks in the past 24 hours across four investing subreddits:

- r/investing
- r/wallstreetbets
- r/pennystocks
- r/stocks

To scrape reddit, this script uses PRAW, or Python Reddit API Wrapper.

The scraper then writes these stock tickers, the times they are mentioned, and the sentiment that the user felt about the stock using VADER (Valence Aware Dictionary and sEntiment Reasoner) to a MongoDB database.

# How to use
1. You must have the tickersSet.pickle file included in this repository in the same directory level as your scraper.py.
2. Change the MongoDB client (on line 25, change the pyMongo client to whatever your client address is, on MongoDB Atlas or otherwise.)
3. Setup a developer account on Reddit so that you are able to use PRAW, and update the reddit object on line 36 to include your credentials. This tutorial: https://www.youtube.com/watch?v=gIZJQmX-55U is fantastic for learning how to get registered and ready to use PRAW.
4. Run the script.
5. Optional: Setup an automated job so that this script runs every night at 12AM (I personally used cron on Ubuntu) so that this script runs every night at 12AM, keeping your data up-to-date. 

Your MongoDB database will now be populated with stock mention data :)

An example of a document that this script writes:

```
{
    _id: ObjectId("63bbd557d7360aaf194bf9b6"),
    name: 'CRM',
    mentions: 2,
    postInfo: [
      {
        postTitle: 'Last month I posted about CRM being the next overvalued tech to crash, Burry agrees!',
        postLink: '/r/wallstreetbets/comments/103tby2/last_month_i_posted_about_crm_being_the_next/',
        sentiment: 'Negative'
      },
      {
        postTitle: 'Salesforce CRM / Tesla',
        postLink: '/r/wallstreetbets/comments/103wdtj/salesforce_crm_tesla/',
        sentiment: 'Neutral'
      }
    ]
  },
```
### What is tickersSet.pickle?
This is a "pickled" hash-set of all stock tickers from the NASDAQ website. "Pickled" means that it is a serialized Python object structure, and that pickle file already contains all of the stock tickers. This is to improve on runtime, so that we don't have to loop through and populate our set with every run of the script, and it is a hash-set so that we can take advantage of the constant lookup time, which also drastically cuts down on our runtime when scraping Reddit.
