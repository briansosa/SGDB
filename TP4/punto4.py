# %%

from database import DB
import pymongo
from pymongo import collection
from pymongo.errors import DocumentTooLarge
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopandas import GeoSeries, GeoDataFrame
import matplotlib.colors as mplc

# %%
WorldDatabase = GeoDataFrame.from_file('./docs/ne_10m_admin_0_countries.shp')
WorldDatabase

# %%
# Connect to MongoDB instance running on localhost
client = pymongo.MongoClient()
db = client['test']
# TweetCollection = db.test
TweetCollection = db.tweets

# %%
b = TweetCollection.find({"id": 1116019536988463104})
for a in b:
    print(a["user"]["location"])

# %%
dfCountryTweets = pd.DataFrame(columns=['country_code', 'country', 'text'])

tweets = TweetCollection.find()
for tweet in tweets:
    # print(tweet["id"])
    location = tweet["user"]["location"]
    if location or location is not None:
        location = location.replace("'", "")
        queryCountry = f"""SELECT name, code FROM country WHERE lower('{location}') LIKE '%'  || lower(name) || '%'"""
        country = DB.SelectRows(queryCountry)
        if len(country) != 0:
            tweet["user"]["country"] = country[0][0]
            tweet["user"]["country_code"] = country[0][1]
        else:
            queryCountryCode = f"""
            SELECT name, code FROM country WHERE lower('{location}') LIKE '%'  || lower(code) || '%'
            """
            country = DB.SelectRows(queryCountryCode)
            if len(country) != 0:
                tweet["user"]["country"] = country[0][0]
                tweet["user"]["country_code"] = country[0][1]
            else:
                queryCity = f"""
                SELECT ci.countrycode country_code, co.name country, ci.name 
                FROM city ci
                INNER JOIN country co ON ci.countrycode = co.code
                WHERE lower('{location}') LIKE '%'  || lower(ci.name) || '%'
                """
                country = DB.SelectRows(queryCity)
                if len(country) != 0:
                    tweet["user"]["country_code"] = country[0][0]
                    tweet["user"]["country"] = country[0][1]
                else:
                    tweet["user"]["country"] = None
                    tweet["user"]["country_code"] = None
    else:
        tweet["user"]["country"] = None
        tweet["user"]["country_code"] = None
    # try:
    data = {'country_code': tweet['user']['country_code'], 'country': tweet['user']['country'], 'text': tweet['text']}
    dfCountryTweets = dfCountryTweets.append(data, ignore_index=True)
    # except BaseException as err:
    #     print(tweet['id'])
    #     print(f"Unexpected {err=}, {type(err)=}")
    #     raise

# %%
dfCountryTweetsCount = dfCountryTweets.groupby(['country_code']).size().reset_index(name='count_tweets')
dfCountryTweetsCount

# %%

WorldDatabaseWithCount = WorldDatabase.merge(
                    right = dfCountryTweetsCount,
                    left_on = 'ADM0_A3',
                    right_on = 'country_code',
                    how = 'left'
                    )
WorldDatabaseWithCount = WorldDatabaseWithCount.drop('country_code', axis=1)

WorldDatabaseWithCount = WorldDatabaseWithCount[WorldDatabaseWithCount['count_tweets'].notnull()]
WorldDatabaseWithCount.head()

# %%
WorldDatabaseWithCount.plot(column='count_tweets', cmap='Reds', alpha=1, linewidth = 0.5, edgecolor='black', figsize = (14,8), categorical=False, legend=False, ax=None)


# %%
dfCountryTweetsWords = dfCountryTweets[dfCountryTweets["country_code"] in ["USA", "ARG"]]


# %%
