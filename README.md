This is a scraper that will find the last most top mentioned stocks in the past 24 hours across four investing subreddits:

- r/investing
- r/wallstreetbets
- r/pennystocks
- r/stocks

The scraper then writes these stock tickers, the times they are mentioned, and the sentiment that the user felt about the stock using VADER (Valence Aware Dictionary and sEntiment Reasoner) to a MongoDB database.

How to use:
1. You must have the tickersSet.pickle file included in this repository in the same directory level as your scraper.py.
2. Change the MongoDB client (on line 25, change the pyMongo client to whatever your client address is, on MongoDB Atlas or otherwise.)
3. Run the script.

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