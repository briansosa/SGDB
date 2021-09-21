import sys
import re
import operator

# 2.2.1.
# Escribir un programa para procesar el archivo “king lear.txt”:
# Pasar las palabras a min´usculas
# Descartar los signos de puntuaci´on
# Separar y contar las ocurrencias de las palabras (Evaluar si conviene utilizar un “dict” o la clase “collections.Counter”
# de python)
# Ordenar de modo descendente las palabras por cantidad de ocurrencias
# Responder
# • ¿Cu´antas palabras tiene el texto?
# • ¿Cu´ales son las 5 palabras m´as usadas?

DATASET = "king_lear-dataset.txt"
#DATASET = "test.txt"

def main():
    # Leer y sanatizar el archivo
    pathFile = "./SGDB/TP1/documentacion/{}".format(DATASET)
    text = ""
    with open(pathFile, 'r') as f:
        text = f.read()
    sanitizeText = replacePunctuationMarks(text.lower())
    listWords = sanitizeText.split()

    # Ocurrencias de las palabras
    dictionaryWords = dict()
    keysInDictionary = list()
    for word in listWords:
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


main()
