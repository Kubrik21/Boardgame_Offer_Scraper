import time

import sqlOperations as db
from merger import merge

import json
import scrapMapel
import scrapShopgracz
import streamlit as st


def scrap_file(x):
    ###block button
    ###label show
    ###count on label

    ###after that enable button
    ###label show
    with st.spinner(text='Scraping data. Wait for it...'):
    # Scrap & save to file
        time.sleep(1)
        try:
            L2=scrapShopgracz.scrap()
        except TimeoutError:
            print("Connection timed out. ")
    # with open("../Shopgracz","w",encoding='utf-8') as file:
    #     json.dump(L2,file, ensure_ascii=False)

    #Sccrap & save to file
        try:
            L1=scrapMapel.scrap()
        except TimeoutError:
            print("Connection timed out. ")

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

        dateID=db.actualize()

        db.unionBoardgames(All)

        db.delete_last(dateID)

        idList=db.get_game_index()

        db.add_offer(All,idList,dateID)
    st.success('Done!')


st.title("Scrap boardgames")
st.write("""
The spider will scrap the offer of two well-known board game stores - mepel.pl and aleplanszówki.pl.
The received data will be merged and sent to the database. The process may take 3-5 minutes
""")
c1,c2,c3=st.columns([3,1.5,3])
with c2:
    st.button(label="Scrap data", on_click=scrap_file, args=(1,))
st.empty()

