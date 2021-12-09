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
b = TweetCollection.find()
for a in b:
    print(a["user"]["country"])
    print(a["user"]["country_code"])

# %%
tweets = TweetCollection.find()
count = 1
for tweet in tweets:
    print(count)
    count += 1
    countryData = ""
    countryCodeData = ""
    location = tweet["user"]["location"]
    if location or location is not None:
        location = location.replace("'", "")
        queryCountry = f"""SELECT name, code FROM country WHERE lower('{location}') LIKE '%'  || lower(name) || '%'"""
        country = DB.SelectRows(queryCountry)
        if len(country) != 0:
            countryData = country[0][0]
            countryCodeData = country[0][1]
        else:
            queryCountryCode = f"""
            SELECT name, code FROM country WHERE lower('{location}') LIKE '%'  || lower(code) || '%'
            """
            country = DB.SelectRows(queryCountryCode)
            if len(country) != 0:
                countryData = country[0][0]
                countryCodeData = country[0][1]
            else:
                queryCity = f"""
                SELECT ci.countrycode country_code, co.name country, ci.name 
                FROM city ci
                INNER JOIN country co ON ci.countrycode = co.code
                WHERE lower('{location}') LIKE '%'  || lower(ci.name) || '%'
                """
                country = DB.SelectRows(queryCity)
                if len(country) != 0:
                    countryCodeData = country[0][0]
                    countryData = country[0][1]
                else:
                    countryData = None
                    countryCodeData = None
    else:
        countryData = None
        countryCodeData = None
    query = {'id': tweet['id']}
    newValue = {'$set': {
        "user.country": countryData,
        "user.country_code": countryCodeData
        }
    }
    TweetCollection.update_one(query, newValue)


# %%
countryTweetsCount = TweetCollection.aggregate([
    { "$group":{"_id":"$user.country_code", "count_tweets": { "$count": {} }} },
    { "$sort": { "count_tweets": -1 } }
])

listCountryTweetsCount = list(countryTweetsCount)
dfCountryTweetsCount = pd.DataFrame(listCountryTweetsCount)
dfCountryTweetsCount

# %%

WorldDatabaseWithCount = WorldDatabase.merge(
                    right = dfCountryTweetsCount,
                    left_on = 'ADM0_A3',
                    right_on = '_id',
                    how = 'left'
                    )
WorldDatabaseWithCount = WorldDatabaseWithCount.drop('_id', axis=1)

WorldDatabaseWithCount = WorldDatabaseWithCount[WorldDatabaseWithCount['count_tweets'].notnull()]
WorldDatabaseWithCount.head()

# %%
WorldDatabaseWithCount.plot(column='count_tweets', cmap='Reds', alpha=1, linewidth = 0.5, edgecolor='black', figsize = (14,8), categorical=False, legend=False, ax=None)


# %%
import re
import operator

dictionaryWordsUSA = dict()
keysInDictionaryUSA = list()

tweetsUSA = TweetCollection.find({'user.country_code': 'USA'})
for tweetUSA in tweetsUSA:
    tweetTextUSA = tweetUSA['text'].lower()
    wordsUSA = re.sub('[.,;:\"\'()¿?¡!-_]', '', tweetTextUSA).split()
    for word in wordsUSA:
        if word not in keysInDictionaryUSA:
            dictionaryWordsUSA[word] = 1
            keysInDictionaryUSA.append(word)
        else:
            dictionaryWordsUSA[word] = dictionaryWordsUSA[word] + 1

sortedWordsByFrecuence = sorted(dictionaryWordsUSA.items(), key=operator.itemgetter(1), reverse=True)
print("El texto contiene {} palabras".format(len(sortedWordsByFrecuence)))
print("Las 20 palabras mas usadas son las siguientes:")
print(sortedWordsByFrecuence[:20])

# %%
from wordcloud import WordCloud

# Nube de palabras
dfWordCloud = pd.DataFrame(sortedWordsByFrecuence[:20], columns=['word', 'frecuence'])
wordcloud = WordCloud().generate(" ".join(dfWordCloud.word))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# %%
