import sys
import re

# 2.1.2.
# Dado un string con el siguiente formato: “nombre1,apellido1,DNI1/.../nombreN,apellidoN,DNIN”, escribir un programa
# que lo procese y escriba la siguiente informaci´on por pantalla:
# apellido1 nombre1
# . . .
# apellidoN nombreN

TEXT = "pepe,sand,11111111,laucha,acosta,22222222,toto,belmonte,33333333"

def main():
    persons = re.findall('([A-Za-z]+),([A-Za-z]+)', TEXT)
    print(persons)
    for person in persons:
        name = person[0]
        lastName = person[1]
        print(lastName + " " + name)

main()