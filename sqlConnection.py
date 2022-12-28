import mysql.connector
from datetime import date

from merger import merge
import json
#
# initial=False
#
# try:
#   mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="123MySql321",
#     database="dbo_boardgamess"
#   )
# except mysql.connector.Error as err:
#
#   initial=True
#   print("Connection error")
#
#
# if initial == True:
#   # Creating DB
#   mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="123MySql321",
#   )
#
#   mycursor = mydb.cursor()
#
#   #createDBO
#   mycursor.execute("CREATE DATABASE dbo_boardgames_temp")

#Usuwanie i tworzenie
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123MySql321",
    database="dbo_boardgames_temp"
  )
mycursor = mydb.cursor(buffered=True)
#   #Create tables
#
# mycursor.execute("DROP TABLE IF EXISTS db_offer")
# mycursor.execute("DROP TABLE IF EXISTS db_boardgames")
# mycursor.execute("DROP TABLE IF EXISTS db_date")
#     #DB_Date
# mycursor.execute("CREATE TABLE db_date (id INT AUTO_INCREMENT PRIMARY KEY, date VARCHAR(255))")
#
#   #DB_Boardgames
# mycursor.execute("CREATE TABLE db_boardgames (id INT AUTO_INCREMENT PRIMARY KEY, boardgame_name VARCHAR(255), img VARCHAR(255))")
#
#   #DB_Offer
# mycursor.execute("CREATE TABLE db_offer (id INT AUTO_INCREMENT PRIMARY KEY, store VARCHAR(255), link VARCHAR(255), price FLOAT(5,2), date_id INT, game_id INT, FOREIGN KEY (date_id) REFERENCES db_date(id), FOREIGN KEY (game_id) REFERENCES db_boardgames(id))")
# print(mydb)


#Actualize
#Pobierz najnowszą datę [DONE]
#jeśli nie ma lub nie dzisiejsza -> A [Done]
#Jeśli jest dzisiejsza -> B [Done]
def actualize():
    today = date.today().strftime("%d-%m-%Y")
    mycursor.execute("SELECT date FROM db_date ORDER BY id DESC LIMIT 1")
    db_date= mycursor.fetchall()
    print(db_date)
    # A
    # Dodaj dzisiejszą datę i zwróć indeks[Done]
    # Pass[Done]

    if db_date == [] or str(db_date[0][0])!=today:
        print(db_date)
        print(today)

        sql="INSERT INTO db_date (date) VALUES (%s)"
        val=(today,)
        mycursor.execute(sql,val)
        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        print(mycursor.lastrowid)
    else:
        # B
        # Przypisz indeksowi dzisiejszą datę[Done]
        #
        # Pass[Done]
        mycursor.execute("SELECT id FROM db_date ORDER BY id DESC LIMIT 1")
        dateID = mycursor.fetchall()
        print("jest")
        print(dateID[0][0])
        pass

    unionBoardgames()

        #Wrzuć do tabeli temp gry i ich zdjęcia[Done]

def unionBoardgames():
    mycursor.execute("DROP TABLE IF EXISTS temp")
    mycursor.execute("CREATE TABLE temp LIKE db_boardgames")
    val=[]
    #Temp
    with open("Mepel", "r", encoding='utf-8') as file:
        L1=file.read()
    with open("Shopgracz", "r", encoding='utf-8') as file:
        L2=file.read()

    All = merge(json.loads(L1), json.loads(L2))
    for elem in All:
        val.append((elem["Name"], elem["Img"]))


    #print(val)
    sql = "INSERT INTO temp (boardgame_name,img) VALUES (%s,%s)"
    mycursor.executemany(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")

    # dodaj tylko to czego brakuje[DONE]
    #Sprawdź czy można pominąć tworzenie tempa i przekazać parametr z listą dla selecta z Not IN
    mycursor.execute("INSERT INTO dbo_boardgames_temp.db_boardgames SELECT * FROM dbo_boardgames_temp.temp B WHERE B.boardgame_name NOT IN (SELECT boardgame_name FROM dbo_boardgames_temp.db_boardgames)")
    mydb.commit()

    # usuń temp[DONE]
    mycursor.execute("DROP TABLE IF EXISTS temp")


#Pobierz nową tabelę gier i jej indeksów
#Usun wszystkie dotychczasowe gry i ich ceny z maina jeśli data jest dzisiejsza
#Dodaj dzisiejsze gry indeksy z innej tabeli


actualize()
