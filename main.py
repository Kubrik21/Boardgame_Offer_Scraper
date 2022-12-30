import requests
from selectorlib import Extractor
from merger import merge

import json
import scrapMapel
import scrapShopgracz


from sqlInit import init
import sqlOperations as db

if __name__ == '__main__':

    #Check if DB exist and setting cursor on DBO
    init()


    #pobierz dane z BD z ostatniej aktualizacji i zmerguj je do prezentacji











