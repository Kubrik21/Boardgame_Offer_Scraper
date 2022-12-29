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


    #Scrap and merge
    #Then actualize

    #L2=scrapShopgracz.scrap()
    #with open("Shopgracz","w",encoding='utf-8') as file:
    #  json.dump(L2,file, ensure_ascii=False)

    L1=scrapMapel.scrap()
    with open("Mepel","w",encoding='utf-8') as file:
      json.dump(L1,file,ensure_ascii=False)

    with open("Mepel", "r", encoding='utf-8') as file:
        L1=file.read()
    with open("Shopgracz", "r", encoding='utf-8') as file:
        L2=file.read()

   # print(json.loads(L2)[1])
    #Merging data - 350 games available on both sites
    All=merge(json.loads(L1),json.loads(L2))
    wyn=0
    for x in range(len(All)):
        wyn+=1
        #print(All[x])
        if len(All[x]['Shop'])!=1:
            wyn+=1
    #print(wyn)








