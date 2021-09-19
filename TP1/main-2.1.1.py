import sys
import re


# 2.1.1.
# Escribir un programa que reconozca los s´ımbolos de los n´umeros romanos: recibe un string S por teclado e imprime
# “TRUE” si todos los caracteres de S corresponden a s´ımbolos de n´umeros romanos o “FALSE” en caso contrario. Por
# ejemplo:
# input: “XL” → output: “TRUE”
# input “#CienciaDeDatos” → output: “FALSE”
# Obs.: no hay que determinar que el n´umero sea v´alido. Por ejemplo el input “IIII” deber´ıa devolver “TRUE”.

def main():
    inputText = ""
    if len(sys.argv) >= 2:
        inputText = sys.argv[1]

    match = re.search('[IiVvXxLlCcDdMm]*', inputText)
    if match:
        if match.group() == inputText:
            print(True)
        else:
            print(False)

main()