import pymongo
from pymongo import collection
from pymongo.errors import DocumentTooLarge
import bson
from bson.son import SON
import re

Collection = None

# Connect to MongoDB instance running on localhost
def connectDatabase():
    client = pymongo.MongoClient()
    db = client['test']
    global Collection
    # Collection = db.test
    Collection = db.tweets

# Ejercicio 1.1
def exercise11():
    documents = Collection.find().limit(10)
    for document in documents:
        print(f"ID: {document['id']}\nText: {document['text']}\n")

# Ejercicio 1.2
def exercise12():
    documents = Collection.distinct('lang')
    for document in documents:
        print(document)

# Ejercicio 1.3
def exercise13():
    documents = Collection.find({
        'user.followers_count': {
            "$gte": 10000 
        }
    })

    for document in documents:
        print(f"""
        ID: {document['id']}
        Name: {document['user']['name']}
        Descripcion: {document['user']['description']}
        Cantidad de seguidores: {document['user']['followers_count']}
        """)

# Ejercicio 1.4
def exercise14():
    documents = Collection.find().sort("user.followers_count", -1).limit(10)

    for document in documents:
        print(f"""
        ID: {document['id']}
        Name: {document['user']['name']}
        Cantidad de seguidores: {document['user']['followers_count']}
        """)


# Ejercicio 2.1
## PREGUNTA: la consigna dice que tenemos que determinar la cantidad de usuario por cada canal.
# Lo que hicimos fue contar por source, no entendimos muy bien la parte de usuario
def exercise21():
    mapper = bson.Code(
        """
            function map() {
                emit(this.source, 1)
            }
        """
    )

    reduce = bson.Code(
        """
        function(key, values) {
            return Array.sum(values)
        }
        """
    )

    mapReduceCollection = Collection.map_reduce(mapper, reduce, "mapReduce")
    documents = mapReduceCollection.find()

    for document in documents:
        print(document)


# Ejercicio 2.2
def exercise22():
    mapper = bson.Code(
        """
            function map() {
                emit(this.lang, 1)
            }
        """
    )

    reduce = bson.Code(
        """
        function(key, values) {
            return Array.sum(values)
        }
        """
    )

    mapReduceCollection = Collection.map_reduce(mapper, reduce, "mapReduce")
    documents = mapReduceCollection.find()

    for document in documents:
        print(document)


# Ejercicio 2.3
## PREGUNTA: ¿Acá habia que usar Map Reduce? Nos sonó raro
### Ver bien el tema del split de las palabras
def exercise23():
    def classifyTweet(tweet):
        listWords = re.compile("([\w][\w]*'?\w?)").findall(text)
        countWords = len(listWords)
        if countWords < 10:
            return "corto"
        elif countWords < 20:
            return "mediano"
        else:
            return "largo"

    classifier = dict()
    documents = Collection.find()
    for document in documents:
        text = document['text']
        classification = classifyTweet(text)
        if classification not in classifier:
            classifier[classification] = 1
        else:
            classifier[classification] = classifier[classification] + 1

    print(classifier)

# Ejercicio 3.1
def exercise31():
    documents = Collection.aggregate([
        { "$group": {"_id": "$user.id", "count": { "$count": {}}} },
        { "$sort": { "count": -1 } },
        { "$limit": 10 }
    ])

    for document in documents:
        print(document)

# Ejercicio 3.2
def exercise32():
    documents = Collection.aggregate([
        { "$group":{"_id":"$user.lang", "maxFollower": { "$max": "$user.followers_count" }} },
        { "$sort": { "maxFollower": -1 } }
    ])

    for document in documents:
        print(document)


def main():
    connectDatabase()
    # exercise11()
    # exercise12()
    # exercise13()
    # exercise14()
    # exercise21()
    # exercise22()
    # exercise23()
    # exercise31()
    exercise32()

main()