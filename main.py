import requests
from selectorlib import Extractor
from merger import merge

import json
import scrapMapel
import scrapShopgracz

#L1=[{"Name":"a","Img":"abc","Link":"abc","Price":10},{"Name":"b","Img":"cde","Link":"cde","Price":12}]
#L2=[{"Name":"b","Img":"bcd","Link":"bcd","Price":11},{"Name":"c","Img":"def","Link":"def","Price":13}]

if __name__ == '__main__':
    # Scrap and saved in file
    L2=scrapShopgracz.scrap()
    with open("Shopgracz","w",encoding='utf-8') as file:
        json.dump(L2,file, ensure_ascii=False)
    # Scrap and saved in file
    L1=scrapMapel.scrap()
    with open("Mepel","w",encoding='utf-8') as file:
        json.dump(L1,file,ensure_ascii=False)

    with open("Mepel", "r", encoding='utf-8') as file:
        L1=file.read()
    with open("Shopgracz", "r", encoding='utf-8') as file:
        L2=file.read()

    #print(L2)
    All=merge(L1,L2)
    for x in range(len(All)):
        print(All[x])








