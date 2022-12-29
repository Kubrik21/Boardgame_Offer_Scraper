import mysql.connector

def init():
#checking connection
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123MySql321")

        mycursor = mydb.cursor()

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
        mycursor = mydb.cursor()
        print("Connection completed. DatabaseObject exist")

    except mysql.connector.Error as err:
        print("DatabaseObject doesn't exist. Creating DatabaseObject and reconnecting")
        mycursor.execute("CREATE DATABASE dbo_boardgames")
        init()

    return(mycursor)

#init()