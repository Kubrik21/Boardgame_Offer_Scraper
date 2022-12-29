import mysql.connector
from datetime import date

from merger import merge
import json

connect=['localhost','root','123MySql321','dbo_boardgames']


def actualize():

    #Get latest date from DBtable
    mycursor.execute("SELECT date FROM db_date ORDER BY id DESC LIMIT 1")
    db_date = mycursor.fetchall()

    #print(db_date)

    #If date doesnt exist or it is different than today's date
    if db_date == [] or str(db_date[0][0]) != today:
        #Add today's date
        sql = "INSERT INTO db_date (date) VALUES (%s)"
        val = (today,)
        mycursor.execute(sql, val)
        mydb.commit()

        #get ID of today's date
        dateID = mycursor.lastrowid


    #If not
    else:
        #Get today's date witch exist in DBO
        mycursor.execute("SELECT id FROM db_date ORDER BY id DESC LIMIT 1")
        dateID = mycursor.fetchall()[0][0]
        #print(dateID)

    #expand the game database with new titles that appeared during the last one scrapping
    unionBoardgames()

    #return dateID
    return dateID

def unionBoardgames():
    #drop temp DB table if exist
    mycursor.execute("DROP TABLE IF EXISTS temp")
    #create new temp table
    mycursor.execute("CREATE TABLE temp LIKE db_boardgames")

    val=[]
    #Temp
    with open("Mepel", "r", encoding='utf-8') as file:
        L1=file.read()
    with open("Shopgracz", "r", encoding='utf-8') as file:
        L2=file.read()

    All = merge(json.loads(L1), json.loads(L2))
    #From every single data row get the name and IMG
    for elem in All:
        val.append((elem["Name"], elem["Img"]))
    #

    #fill the temp table
    sql = "INSERT INTO temp (boardgame_name,img) VALUES (%s,%s)"
    mycursor.executemany(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "was inserted.")

    #Add to existing main, boardgame' database nonexistend rows
    mycursor.execute("INSERT INTO db_boardgames SELECT * FROM temp B WHERE B.boardgame_name NOT IN (SELECT boardgame_name FROM db_boardgames)")
    mydb.commit()

    #drop temp table
    mycursor.execute("DROP TABLE IF EXISTS temp")

#If we scrap data two or more times. Delete today's data
def delete_last(date_id):
    sql="DELETE FROM db_offer WHERE date_id = (%s)"
    val=date_id
    mycursor.execute(sql,val)
    mydb.commit()

#Download bg's names and ID's. Return List of tuples
def get_game_index():
    mycursor.execute("SELECT id,boardgame_name FROM db_boardgames")
    gameID = mycursor.fetchall()
    print(gameID)
    return gameID

#Fill db_offer table
def add_offer(bgList,gameID,dateID):

    val=[]
    #For every single element from list of scrapped data
    for elem in bgList:
        #for every single element from list of Shop's
        for el in elem["Shop"]:
            #Get existing BG ID
            try:
                bgID, item_name = next(item for item in gameID if item[1] == elem["Name"])
            except StopIteration:
                print(f'Could not find{item_name}.')
                bgID=None

            #if bgID exist then create data tuple
            if bgID!=None:
                try:
                    tup=(el["Shop_name"],el["Link"],float(el["Price"]),dateID,bgID)
                    #.replace(',', '.').replace(' ','')
                except ValueError:
                    print(el["Shop_name"],elem["Name"])
            #create list of tuples
                val.append(tup)
    #Insert data to DBO
    sql="INSERT INTO db_offer (store,link,price,date_id,game_id) VALUES (%s,%s,%s,%s,%s)"

    try:
        mycursor.executemany(sql,val)

    except mysql.connector.Error:
        print("Error with inserting data to DBO")

    mydb.commit()

#get whole data which dateID = x
def get_data(dateID):
    sql="SELECT b.boardgame_name, b.img, o.store, o.link, o.price FROM db_offer o JOIN db_boardgames AS b ON o.game_id = b.id WHERE o.date_id=%s"
    #val=(dateID,)
    val=(2,)

    mycursor.execute(sql,val)
    offerList = mycursor.fetchall()

    return offerList


if __name__== '__main__':

    mydb = mysql.connector.connect(
        host=connect[0],
        user=connect[1],
        password=connect[2],
        database=connect[3],
    )
    mycursor = mydb.cursor(buffered=True)

    today = date.today().strftime("%d-%m-%Y")

    # fill bd_date and db_boardgame
    idDate = actualize()

    # List of bg indexes
    # listOfID=get_game_index()