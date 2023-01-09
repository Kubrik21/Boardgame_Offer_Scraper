import sqlOperations as db
import streamlit as st
import webbrowser
import altair as alt
import pandas as pd
import datetime

def dateIndex():
    dates=[]
    for num in range(0,7):
        prevDay = datetime.date.today() - datetime.timedelta(days=6-num)
        prevDay = prevDay.strftime("%Y-%m-%d")
        dates.append(prevDay)
    return dates

def prepare_data(dateIndex,shop):
    data={'Mepel.pl':[None,None,None,None,None,None,None],
          'Shopgracz.pl':[None,None,None,None,None,None,None]}

    urlA=urlB=""

    for elem in shop:
        index=dateIndex.index(str(elem[6]))
        if(elem[3]=='mepel.pl'):
            data['Mepel.pl'][index]=elem[5]
            urlA=elem[4]
        else:
            data['Shopgracz.pl'][index]=elem[5]
            urlB=elem[4]
        # print(datetime.datetime(2013, 1, 12).date())

    df=pd.DataFrame(
        {
            'Date':dateIndex,
            'Mepel.pl':data['Mepel.pl'],
            'Shopgracz.pl':data['Shopgracz.pl']
        },
        columns=["Date","Mepel.pl","Shopgracz.pl"]
    )
    return df,urlA,urlB


st.markdown("""
    <style>
    .space-history{
    min-height:25px;
    }
    </style>
    """, unsafe_allow_html=True)


def main():

    List = db.get_game_index()
    list_tuple = [ (item[1]) for item in List ]

    st.selectbox(label="Search game",options=list_tuple, key="selectbox")
    st.markdown('<p class="space-history"></p>',unsafe_allow_html=True)
    print( st.session_state['selectbox'])

    if(st.session_state['selectbox']!=None):
        for elem in List:
            if elem[1] == st.session_state['selectbox'] :
                index=elem[0]
                print(index)
                statisticList = db.game_stats(index)

    print(statisticList)

    if(len(statisticList)>0):
        img=statisticList[0][2]
        sevenDays=dateIndex()

        # prepare data
        raw,urlA,urlB=prepare_data(sevenDays,statisticList)
        # print(raw)

        raw = raw.melt('Date', var_name='Store', value_name='Price')

        chart = alt.Chart(raw).mark_line(point=True).encode(
            x=alt.X('Date:N'),
            y=alt.Y('Price:Q'),
            color=alt.Color("Store:N")
        ).properties(title="Price history   ")

        st.altair_chart(chart, use_container_width=True)
        st.markdown('<p class="space-history"></p>',unsafe_allow_html=True)

        c1,c2,c3=st.columns([2,3,2])

        with c1:
            st.write("Mepel.pl")
            if urlA=='': offA=True
            else: offA=False
            st.button(label="Check offer",on_click=webbrowser.open_new_tab, args=(urlA,),disabled=offA,key="historyA")

        with c3:

            st.write("Shopgracz.pl")
            if urlB=='': offB = True
            else: offB=False
            st.button(label="Check offer",on_click=webbrowser.open_new_tab, args=(urlB,),disabled=offB,key="historyB")
main()


