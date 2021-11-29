import pymongo
from pymongo import collection
from pymongo.errors import DocumentTooLarge
import bson
from bson.son import SON
import re


# Connect to MongoDB instance running on localhost
client = pymongo.MongoClient()
db = client['test']
# collection = db.test
collection = db.tweets

# Ejercicio 1.1
# documents = collection.find().limit(10)
# for document in documents:
#     print(f"ID: {document['id']}\nText: {document['text']}\n")

# Ejercicio 1.2
# documents = collection.distinct('lang')
# for document in documents:
#     print(document)

# Ejercicio 1.3
# documents = collection.find({
#     'user.followers_count': {
#         "$gte": 10000 
#     }
# })

# for document in documents:
#     print(f"""
#     ID: {document['id']}
#     Name: {document['user']['name']}
#     Descripcion: {document['user']['description']}
#     Cantidad de seguidores: {document['user']['followers_count']}
#     """)

# Ejercicio 1.4
# documents = collection.find().sort("user.followers_count", -1).limit(10)

# for document in documents:
#     print(f"""
#     ID: {document['id']}
#     Name: {document['user']['name']}
#     Cantidad de seguidores: {document['user']['followers_count']}
#     """)


# Ejercicio 2.1

## PREGUNTA: la consigna dice que tenemos que determinar la cantidad de usuario por cada canal.
# Lo que hicimos fue contar por source, no entendimos muy bien la parte de usuario

# mapper = bson.Code(
#     """
#         function map() {
#             emit(this.source, 1)
#         }
#     """
# )

# reduce = bson.Code(
#     """
#     function(key, values) {
#         return Array.sum(values)
#     }
#     """
# )

# mapReduceCollection = collection.map_reduce(mapper, reduce, "mapReduce")
# documents = mapReduceCollection.find()

# for document in documents:
#     print(document)


# Ejercicio 2.2

# mapper = bson.Code(
#     """
#         function map() {
#             emit(this.lang, 1)
#         }
#     """
# )

# reduce = bson.Code(
#     """
#     function(key, values) {
#         return Array.sum(values)
#     }
#     """
# )

# mapReduceCollection = collection.map_reduce(mapper, reduce, "mapReduce")
# documents = mapReduceCollection.find()

# for document in documents:
#     print(document)


# Ejercicio 2.3
## PREGUNTA: ¿Acá habia que usar Map Reduce? Nos sonó raro
### Ver bien el tema del split de las palabras

# def classifyTweet(tweet):
#     listWords = re.compile("([\w][\w]*'?\w?)").findall(text)
#     countWords = len(listWords)
#     if countWords < 10:
#         return "corto"
#     elif countWords < 20:
#         return "mediano"
#     else:
#         return "largo"

# classifier = dict()
# documents = collection.find()
# for document in documents:
#     text = document['text']
#     classification = classifyTweet(text)
#     if classification not in classifier:
#         classifier[classification] = 1
#     else:
#         classifier[classification] = classifier[classification] + 1

# print(classifier)

# Ejercicio 3.1
# documents = collection.aggregate([
#     { "$group": {"_id": "$user.id", "count": { "$count": {}}} },
#     { "$sort": { "count": -1 } },
#     { "$limit": 10 }
# ])

# for document in documents:
#     print(document)

# Ejercicio 3.2
documents = collection.aggregate([
    { "$group":{"_id":"$user.lang", "maxFollower": { "$max": "$user.followers_count" }} },
    { "$sort": { "maxFollower": -1 } }
])

for document in documents:
    print(document)

