import mysql.connector
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
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123MySql321",
    database="dbo_boardgames_temp"
  )
mycursor = mydb.cursor()
  #Create tables

mycursor.execute("DROP TABLE IF EXISTS db_offer")
mycursor.execute("DROP TABLE IF EXISTS db_boardgames")
mycursor.execute("DROP TABLE IF EXISTS db_date")
    #DB_Date
mycursor.execute("CREATE TABLE db_date (id INT AUTO_INCREMENT PRIMARY KEY, date VARCHAR(255))")

  #DB_Boardgames
mycursor.execute("CREATE TABLE db_boardgames (id INT AUTO_INCREMENT PRIMARY KEY, boardgame_name VARCHAR(255), img VARCHAR(255))")

  #DB_Offer
mycursor.execute("CREATE TABLE db_offer (id INT AUTO_INCREMENT PRIMARY KEY, store VARCHAR(255), link VARCHAR(255), price FLOAT(5,2), date_id INT, game_id INT, FOREIGN KEY (date_id) REFERENCES db_date(id), FOREIGN KEY (game_id) REFERENCES db_boardgames(id))")
print(mydb)


#Actualize





