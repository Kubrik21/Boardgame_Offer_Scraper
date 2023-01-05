import mysql.connector
import datetime


con=['localhost','root','123MySql321','dbo_boardgames']
def connect():
    mydb = mysql.connector.connect(
        host=con[0],
        user=con[1],
        password=con[2],
        database=con[3],
    )
    #mycursor = mydb.cursor(buffered=True)
    return mydb

def actualize():

    mydb=connect()
    mycursor = mydb.cursor(buffered=True)

    today = datetime.date.today().strftime("%Y-%m-%d")

    #Get latest date from DBtable
    mycursor.execute("SELECT scrapDate FROM db_date ORDER BY id DESC LIMIT 1")
    db_date = mycursor.fetchall()

    #print(db_date)

    #If date doesnt exist or it is different than today's date
    if db_date == [] or str(db_date[0][0]) != today:
        #Add today's date
        sql = "INSERT INTO db_date (scrapDate) VALUES (%s)"
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


    #return dateID
    return dateID

def unionBoardgames(List):

    mydb = connect()
    mycursor = mydb.cursor(buffered=True)

    #drop temp DB table if exist
    mycursor.execute("DROP TABLE IF EXISTS dbo_boardgames.temp")
    #create new temp table
    mycursor.execute("CREATE TABLE temp LIKE dbo_boardgames.db_boardgames")

    val=[]
    #Temp
    # with open("Mepel", "r", encoding='utf-8') as file:
    #     L1=file.read()
    # with open("Shopgracz", "r", encoding='utf-8') as file:
    #     L2=file.read()

    # All = merge(json.loads(L1), json.loads(L2))
    #From every single data row get the name and IMG
    for elem in List:
        val.append((elem["Name"], elem["Img"]))
    #

    #fill the temp table
    sql = "INSERT INTO temp (boardgame_name,img) VALUES (%s,%s)"
    mycursor.executemany(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "was inserted.")

    #Add to existing main, boardgame' database nonexistend rows
    mycursor.execute("INSERT INTO dbo_boardgames.db_boardgames (boardgame_name,img) SELECT B.boardgame_name,B.img FROM dbo_boardgames.temp B WHERE B.boardgame_name NOT IN (SELECT boardgame_name FROM dbo_boardgames.db_boardgames)")
    mydb.commit()

    #drop temp table
    mycursor.execute("DROP TABLE IF EXISTS temp")

#If we scrap data two or more times. Delete today's data
def delete_last(date_id):

    mydb = connect()
    mycursor = mydb.cursor(buffered=True)

    sql="DELETE FROM db_offer WHERE date_id = (%s)"
    val=(date_id,)
    mycursor.execute(sql,val)
    mydb.commit()

#Download bg's names and ID's. Return List of tuples
def get_game_index():
    mydb = connect()
    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("SELECT id,boardgame_name FROM db_boardgames")
    gameID = mycursor.fetchall()
    # print(gameID)
    return gameID

#Fill db_offer table
def add_offer(bgList,gameID,dateID):

    mydb = connect()
    mycursor = mydb.cursor(buffered=True)

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


def get_latest_date():

    mydb = connect()
    mycursor = mydb.cursor(buffered=True)


    mycursor.execute("SELECT scrapDate FROM db_date ORDER BY id DESC LIMIT 1")
    dateName = mycursor.fetchall()[0][0]


    return dateName


def games_last_actualize(date):
    mydb = connect()
    mycursor = mydb.cursor(buffered=True)


    sql = """
        SELECT o.id, b.boardgame_name, b.img , o.store, o.link, o.price,d.scrapDate FROM dbo_boardgames.db_offer AS o
        INNER JOIN dbo_boardgames.db_date AS d ON d.id = o.date_id
        INNER JOIN dbo_boardgames.db_boardgames AS b ON b.id = o.game_id
        where d.scrapDate>=(%s); """
    val = (date,)

    mycursor.execute(sql, val)
    latestGames = mycursor.fetchall()

    return latestGames


def game_stats(gameID):

    mydb = connect()
    mycursor = mydb.cursor(buffered=True)

    prevDay = datetime.date.today() - datetime.timedelta(days=6)
    prevDay=prevDay.strftime("%Y-%m-%d")


    sql = """
    SELECT o.id, b.boardgame_name, b.img , o.store, o.link, o.price,d.scrapDate FROM dbo_boardgames.db_offer AS o
    INNER JOIN dbo_boardgames.db_date AS d ON d.id = o.date_id
    INNER JOIN dbo_boardgames.db_boardgames AS b ON b.id = o.game_id
    where d.scrapDate>=(%s) AND b.id=%s; """

    val = (prevDay,gameID)

    mycursor.execute(sql, val)
    gamesFromInterval = mycursor.fetchall()

    return gamesFromInterval

if __name__== '__main__':

    mydb = mysql.connector.connect(
        host=con[0],
        user=con[1],
        password=con[2],
        database=con[3],
    )
    mycursor = mydb.cursor(buffered=True)

    today = datetime.date.today().strftime("%Y-%m-%d")

    # fill bd_date and db_boardgame
    #idDate = actualize()

    #game_stats(2)
    # List of bg indexes
    # listOfID=get_game_index()