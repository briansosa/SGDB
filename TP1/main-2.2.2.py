import sys
import re
import operator

#Escribir un programa basado en el punto anterior que considere filtrar el texto mediante un archivo de “palabras prohibidas”. 
# Más precisamente: se requiere crear un archivo de texto que contenga una palabra por lı́nea y aquellas palabras de “king lear.txt” que estén contenidas en dicho
# archivo deben ser descartadas.
#El objetivo de este proceso de filtrado es descartar aquellas palabras que aportan poca información sobre un texto (ej.: adverbios, artı́culos, proposiciones).


DATASET = "king_lear-dataset.txt"
DATASETPROHIBIDAS = "palabras-prohibidas.txt"


def main():
    # Leer y sanatizar el archivo

    pathFile = "./SGDB/TP1/documentacion/{}".format(DATASET)

    text = ""

 
    with open(pathFile,'r') as g:
        text = g.read()
        
    sanitizeText = replacePalabrasProhibidas(text)
    print(sanitizeText)


def replacePalabrasProhibidas(textToBeReplace):
    pathFileProhibidas = "./SGDB/TP1/documentacion/{}".format(DATASETPROHIBIDAS)
    textProhibidas = ""

    with open(pathFileProhibidas, 'r') as f:
        textProhibidas = f.read()

    return re.sub(textToBeReplace, "")

main()