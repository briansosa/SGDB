from database import DB
import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from geopandas import GeoSeries, GeoDataFrame
import matplotlib.colors as mplc

REPOSITORY_PATH = os.path.dirname(os.path.realpath(__file__))
FILE = 'top-1m.csv'

def main():
    codes = DB.SelectRows("SELECT code2, code FROM country")
    dicCodes = dict(codes)

    pathFile = "{}/files/{}".format(REPOSITORY_PATH, FILE)
    with open(pathFile, 'r') as f:
        dataToInsert = []
        csvReader = csv.DictReader(f, fieldnames=['orderNumber', 'domain'])
        for row in csvReader:
            order = row['orderNumber']
            domain = row['domain']
            domainData = domain.split('.')
            entity = domainData[0]
            country = None
            code = None
            lenDomain = len(domainData) 

            # E.g: positronrt.com.br
            if lenDomain > 2:
                entityType = domainData[1]
                country = domainData[2]
                if country.upper() in dicCodes:
                    code = dicCodes[country.upper()]
            # E.g: weibo.fr / google.com
            elif lenDomain == 2:
                lastElem = domainData[1]
                lenLastElem = len(lastElem)
                ## Si el último elemento tiene dos letras es un país (en casi todos los casos) 
                if lenLastElem == 2:
                    country = lastElem
                    if country.upper() in dicCodes:
                        code = dicCodes[country.upper()]
                ## Si tiene 3 significa que puede ser un com/org..etc. Por default ponemos país US
                elif lenLastElem == 3:
                    entityType = lastElem
                    country = 'US'
                    code = dicCodes[country]
            dataToInsert.append((order, entity, entityType, country, code))        
        DB.InsertSitio(dataToInsert)

main()