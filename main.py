from sqlInit import init
import sqlOperations as db
import streamlit as st
import listAvailableGames as la
import webbrowser


st.set_page_config(page_title="Boardgame's scrapper", layout="wide")

if 'iterator' not in st.session_state:
    st.session_state['iterator'] = 1

def next_page(where):
    temp=st.session_state[where]
    temp+=1
    st.session_state[where]=temp


def prev_page(where):
    temp=st.session_state[where]
    if temp!=1:
        temp-=1
        st.session_state[where]=temp

@st.cache
def initialize():
    init()



@st.cache
def get_last_scrape():
    date = db.get_latest_date()
    result = db.games_last_actualize(date)
    return date,result

if __name__ == '__main__':


    #Check if DB exist and setting cursor on DBO

    initialize()

    st.title("Available boardgames")

    col1,col2=st.columns([3,1])

    #Get data from last scrap

    # date=db.get_latest_date()
    # List=db.games_last_actualize(date)
    date,List=get_last_scrape()

    partOfList=la.merge(List)[((st.session_state["iterator"]-1)*9):st.session_state["iterator"]*9]

    #print(partOfList)


    with col2:
        st.write("last actualisation:",date)

    #Listing
    # Listing
    # for index, elem in enumerate(partOfList):
    for num in range(0, 3):
        with st.container():
            # st.write('to kontener')
            print(num)
            c1, c2,c3 = st.columns(3)

            with c1:
                st.markdown(partOfList[num*3]["Name"])
                st.image(image=partOfList[num*3]["Img"])
                for id, elem in enumerate(partOfList[num*3]["Shop"]):
                    st.write(f"Sklep {elem['Shop_name']}  -  {elem['Price']} zł.")
                    # st.write(f"Cena: {elem['Price']} zł.")
                    # print(f"page_{st.session_state['iterator']}_pos_{num*3}_elem_{id}")
                    st.button(label="Przejdź do oferty", on_click=webbrowser.open_new_tab, args=(elem["Link"],),key=f"page_{st.session_state['iterator']}_pos_{num*3}_elem_{id}")
            with c2:
                st.markdown(partOfList[(num*3)+1]["Name"])
                st.image(image=partOfList[(num*3)+1]["Img"])
                for id,elem in enumerate(partOfList[(num*3)+1]["Shop"]):
                    st.write(f"Sklep {elem['Shop_name']}  -  {elem['Price']} zł.")
                    # st.write(f"Cena: {elem['Price']} zł.")
                    # print(f"page_{st.session_state['iterator']}_pos_{(num*3)+1}_elem_{id}")
                    st.button(label="Przejdź do oferty", on_click=webbrowser.open_new_tab, args=(elem["Link"],),key=f"page_{st.session_state['iterator']}_pos_{(num*3)+1}_elem_{id}")
            with c3:
                st.markdown(partOfList[(num*3)+2]["Name"])
                st.image(image=partOfList[(num*3)+2]["Img"])
                for id,elem in enumerate(partOfList[(num*3)+2]["Shop"]):
                    st.write(f"Sklep {elem['Shop_name']}  -  {elem['Price']} zł.")
                    # st.write(f"Cena: {elem['Price']} zł.")
                    # print(f"page_{st.session_state['iterator']}_pos_{(num*3)+2}_elem_{id}")
                    st.button(label="Przejdź do oferty", on_click=webbrowser.open_new_tab, args=(elem["Link"],),key=f"page_{st.session_state['iterator']}_pos_{(num*3)+2}_elem_{id}")


    col3,col4,col5,col6,col7=st.columns([3,2,1,2,3])

    st.markdown("""
    <style>
    .page-number {
        font-size:400px;
    }
    </style>
    """, unsafe_allow_html=True)


    with col4:
         st.button(label="Prev page", on_click=prev_page, args=("iterator",), key="prev")
    with col5:
        st.markdown(f'<p class="big-font">{st.session_state.iterator}</p>', unsafe_allow_html=True)
        #st.write(st.session_state.iterator)
    with col6:
         st.button(label="Next page", on_click=next_page, args=("iterator",),key="next")


