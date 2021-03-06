import sys
import re
import operator
import os

#Escribir un programa basado en el punto anterior que considere filtrar el texto mediante un archivo de “palabras prohibidas”. 
# Más precisamente: se requiere crear un archivo de texto que contenga una palabra por lı́nea y aquellas palabras de “king lear.txt” que estén contenidas en dicho
# archivo deben ser descartadas.
#El objetivo de este proceso de filtrado es descartar aquellas palabras que aportan poca información sobre un texto (ej.: adverbios, artı́culos, proposiciones).


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

def replacePunctuationMarks(text):
    return re.sub('[.,;:\"\'()¿?¡!-_]', '', text)

def openFile(path):
    file = ""
    with open(path, 'r') as f:
        file = f.read()
    return file


main()


# Para la nube de palabras usar la lib seaborn