import mysql.connector

def init():
#checking connection
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123MySql321")

        mycursor = mydb.cursor(buffered=True)

        print("Database Exist")

    except mysql.connector.Error as err:
        print("Connection error. Check login data")
        exit()

#Checking if database exist
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123MySql321",
            database="dbo_boardgames"
        )
        mycursor = mydb.cursor(buffered=True)

        print("Connection completed. DatabaseObject exist")

    except mysql.connector.Error as err:
        print("DatabaseObject doesn't exist. Creating DatabaseObject and reconnecting")

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123MySql321")

        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("CREATE DATABASE dbo_boardgames")

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123MySql321",
            database="dbo_boardgames"
        )

        mycursor = mydb.cursor(buffered=True)

        # Drop and Create

        mycursor.execute("DROP TABLE IF EXISTS db_offer")
        mycursor.execute("DROP TABLE IF EXISTS db_boardgames")
        mycursor.execute("DROP TABLE IF EXISTS db_date")

        # DB_Date
        mycursor.execute("CREATE TABLE db_date (id INT AUTO_INCREMENT PRIMARY KEY, date VARCHAR(255))")

        # DB_Boardgames
        mycursor.execute("CREATE TABLE db_boardgames (id INT AUTO_INCREMENT PRIMARY KEY, boardgame_name VARCHAR(255), img VARCHAR(255))")

        # DB_Offer
        mycursor.execute("CREATE TABLE db_offer (id INT AUTO_INCREMENT PRIMARY KEY, store VARCHAR(255), link VARCHAR(255), price FLOAT(7,2), date_id INT, game_id INT, FOREIGN KEY (date_id) REFERENCES db_date(id), FOREIGN KEY (game_id) REFERENCES db_boardgames(id))")

        init()


#init()