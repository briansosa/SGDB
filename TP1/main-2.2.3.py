import sys
import re
import operator
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# Realizar las siguientes visualizaciones:
# Un histograma de las 10 palabras representativas con mayor cantidad de ocurrencias en \king lear.txt" (Ver seccion
# "Bar Charts", pag. 75 y 97))
# Una nube de palabras de las 50 palabras mas representativas con mayor cantidad de ocurrencias en \king lear.txt"
# (Ver captulo 20 del libro, pag. 334-336)
# El objetivo de estas visualizaciones es intentar determinar algunas caractersticas esenciales (ej.: el tema, los personajes,
# las acciones) del texto en base a la cantidad de ocurrencias de las palabras.
# Obs.: la nocion de \palabra representativa" es subjetiva por lo tanto queda a criterio personal. Al menos habra que ltrar
# los adverbios, los artculos y las proposiciones.

DATASET = "king_lear-dataset.txt"
# DATASET = "test.txt"
DATASET_PROHIBIDAS = "palabras-prohibidas.txt"
REPOSITORY_PATH = os.path.dirname(os.path.realpath(__file__))



def main():
    # Leer y sanatizar el archivo
    pathFile = "{}/documentacion/{}".format(REPOSITORY_PATH, DATASET)
    text = openFile(pathFile).lower()

    pathFileProhibidas = "{}/documentacion/{}".format(REPOSITORY_PATH, DATASET_PROHIBIDAS)
    textProhibidas = openFile(pathFileProhibidas).lower().split()

    listWords = replacePunctuationMarks(text).split()

    # Ocurrencias de las palabras
    dictionaryWords = dict()
    keysInDictionary = list()
    for word in listWords:
        if word not in textProhibidas:
            if word not in keysInDictionary:
                dictionaryWords[word] = 1
                keysInDictionary.append(word)
            else:
                dictionaryWords[word] = dictionaryWords[word] + 1

    # Se ordena el diccionario
    # primero se obtiene las palabras en tuplas
    # despues se indica que tome el segundo valor de la tupla, en nuestro caso la frecuencia
    # por último se indica que ordene ese valor de forma descendiente
    sortedWordsByFrecuence = sorted(dictionaryWords.items(), key=operator.itemgetter(1), reverse=True)
    print("El texto contiene {} palabras".format(len(sortedWordsByFrecuence)))
    print("Las 5 palabras mas usadas son las siguientes:")
    print(sortedWordsByFrecuence[:5])

    # Se crea un dataFrame con pandas y se le pasa los 10 palabras con mayor frecuencia y se categoriza las columnas
    # Despues se setea el grafico de barras y se muesta
    # dfBarChart = pd.DataFrame(sortedWordsByFrecuence[:10], columns=['word', 'frecuence'])
    # sns.set_theme(style="whitegrid")
    # ax = sns.barplot(x="word", y="frecuence", data=dfBarChart)
    # plt.show()

    # Nube de palabras
    dfWordCloud = pd.DataFrame(sortedWordsByFrecuence[:50], columns=['word', 'frecuence'])
    wordcloud = WordCloud().generate(" ".join(dfWordCloud.word))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


# RECORDATORIO IMPORTANTE:
#  Para ejecutar esto, se puede hacer desde replit:
#  https://replit.com/@BrianSosa1/SGDB#TP1/main-2.2.3.py
#  Se abre este archivo y en la consola se va a Shell y se ejecuta:
#  python3 ./TP1/main-2.2.3.py y listo
#  si rompe por las lib, correr pip3 install <lib>
#  Hay que jugar comentando los dos graficos porque no pudimos hacer correr los dos juntos



def replacePunctuationMarks(text):
    return re.sub('[.,;:\"\'()¿?¡!-_]', '', text)

def openFile(path):
    file = ""
    with open(path, 'r') as f:
        file = f.read()
    return file


main()

