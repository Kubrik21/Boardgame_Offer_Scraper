#scrap 2 shops
#progress bar
#merge and send to DB



import sqlOperations as db
from merger import merge

import json
import scrapMapel
import scrapShopgracz

def scrap_file():

    # Scrap & save to file
    #
    L2=scrapShopgracz.scrap()
    # with open("../Shopgracz","w",encoding='utf-8') as file:
    #     json.dump(L2,file, ensure_ascii=False)

    #Sccrap & save to file

    L1=scrapMapel.scrap()
    # with open("../Mepel","w",encoding='utf-8') as file:
    #     json.dump(L1,file,ensure_ascii=False)

    #Read from file

    # with open("Mepel", "r", encoding='utf-8') as file:
    #     L1 = file.read()
    # with open("Shopgracz", "r", encoding='utf-8') as file:
    #     L2 = file.read()

    #Merging lists

    #All = merge(json.loads(L1), json.loads(L2))
    All = merge(L1, L2)
    with open("../MergedData","w",encoding='utf-8') as file:
       json.dump(All,file,ensure_ascii=False)

    #Send if file exist to DB
    #Fix
    dateID=db.actualize(All)

    db.delete_last(dateID)

    idList=db.get_game_index()

    db.add_offer(All,idList,dateID)


scrap_file()
