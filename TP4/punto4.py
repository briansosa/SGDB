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
WorldDatabase.head()

# a = WorldDatabase[WorldDatabase['ADM0_A3'] == 'GBR']
# a
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
for tweet in tweets[86380:]:
    print(count)
    count += 1
    countryData = ""
    countryCodeData = ""
    location = tweet["user"]["location"]
    if location or location is not None:
        location = re.sub('[^a-zA-Z0-9]+', ' ', location)
        queryCountry = f"""
        SELECT name, code 
        FROM country 
        WHERE COALESCE(TRIM(name), '') <> ''
            AND COALESCE(TRIM(code), '') <> ''
            AND (lower(name) LIKE '%'  || lower('{location}') || '%' 
            OR lower('{location}') LIKE '%'  || lower(name) || '%'
            OR lower(code) LIKE '%' || lower('{location}') || '%')
        """
        country = DB.SelectRows(queryCountry)
        if len(country) != 0:
            countryData = country[0][0]
            countryCodeData = country[0][1]
        else:
            queryCity = f"""
            SELECT ci.countrycode country_code, co.name country 
            FROM city ci
            INNER JOIN country co ON ci.countrycode = co.code
            WHERE COALESCE(TRIM(ci.name), '') <> ''
                AND COALESCE(TRIM(ci.district), '') <> ''
                AND (LOWER(ci.name) LIKE '%' || LOWER('{location}') || '%'
                OR LOWER('{location}') LIKE '%'  || LOWER(ci.name) || '%'
                OR LOWER(ci.district) LIKE '%' || LOWER('{location}') || '%'
                OR LOWER('{location}') LIKE '%'  || LOWER(ci.district) || '%')
            """
            country = DB.SelectRows(queryCity)
            if len(country) != 0:
                countryCodeData = country[0][0]
                countryData = country[0][1]
            else:
                dfLocationCountry = WorldDatabase[
                    WorldDatabase['ADMIN'].str.contains(location)
                    | WorldDatabase['ADMIN'].apply(lambda row: location.find(row) != -1)]
                if dfLocationCountry.empty == False:
                    countryCodeData = WorldDatabase.iloc[0]['ADM0_A3']
                    countryData = WorldDatabase.iloc[0]['ADMIN']
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
WorldDatabaseWithCount['count_tweets2'] =  np.log2(WorldDatabaseWithCount['count_tweets'])
WorldDatabaseWithCount.plot(column='count_tweets2', cmap='Reds', alpha=1, linewidth = 0.5, edgecolor='black', figsize = (14,8), categorical=False, legend=False, ax=None)

# %%
def countWordByFrecuence(tweets):
    dictionaryWords = dict()
    keysInDictionary = list()
    count = 1
    for tweet in tweets:
        print(count)
        count += 1
        tweetText = tweet['text'].lower()
        words = re.sub('[.,;:\"\'()¿?¡!-_]', '', tweetText).split()
        for word in words:
            if word not in keysInDictionary:
                dictionaryWords[word] = 1
                keysInDictionary.append(word)
            else:
                dictionaryWords[word] = dictionaryWords[word] + 1
    return dictionaryWords

# %%
from wordcloud import WordCloud

# Nube de palabras
def plotWordCloud(wordsByFrecuence):
    dfWordCloud = pd.DataFrame(wordsByFrecuence[:20], columns=['word', 'frecuence'])
    wordcloud = WordCloud().generate(" ".join(dfWordCloud.word))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


# %%
import re
import operator

tweetsUSA = TweetCollection.find({'user.country_code': 'USA'})
dictionaryWordsUSA = countWordByFrecuence(tweetsUSA)


sortedWordsByFrecuence = sorted(dictionaryWordsUSA.items(), key=operator.itemgetter(1), reverse=True)
print("El texto contiene {} palabras".format(len(sortedWordsByFrecuence)))
print("Las 20 palabras mas usadas son las siguientes:")
print(sortedWordsByFrecuence[:20])





# %%
