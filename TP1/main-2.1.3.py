import sys
import re

# 2.1.3.
# Escribir un programa que elimine los signos de puntuaci´on de un string.

def main():
    inputText = ""
    if len(sys.argv) >= 2:
        inputText = sys.argv[1]
    replace = re.sub('[.,;:\"\'()¿?¡!-_]', '', inputText)
    print(replace)

main()
