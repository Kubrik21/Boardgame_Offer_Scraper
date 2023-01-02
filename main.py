from sqlInit import init
import sqlOperations as db

if __name__ == '__main__':

    #Check if DB exist and setting cursor on DBO
    init()

    #Get data from last scrap
    date=db.get_latest_date()
    List=db.games_last_actualize(date)

    print(List)



