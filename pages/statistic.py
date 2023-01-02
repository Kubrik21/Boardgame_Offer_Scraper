import sqlOperations as db

def main():

    List = db.get_game_index()

    #Elem to wybór dowolnej gry- indeks z listy
    elem=2

    #then Q to DB for data from last 7 days
    statisticList=db.game_stats(elem)

    #create plotly




