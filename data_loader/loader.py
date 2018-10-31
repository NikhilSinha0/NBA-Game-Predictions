import pymongo
import getpass

def main():
    username = input("Username: ")
    pswd = getpass.getpass('Password:')
    client = pymongo.MongoClient("mongodb+srv://"+username+":"+pswd+"@nsp-cluster-zqniz.mongodb.net/test?retryWrites=true")
    game_records = client["NBA-Game-Data"]["Game-Records"]
    recs = game_records.find(
        {
            "Date": {
                "$lt": "2017/10/30"
            }
        }
    ).sort([("Date", pymongo.DESCENDING)]).limit(5)
    for item in recs2:
        print(item["Home"]["Name"] + " vs " item["Away"]["Name"])

def get_games_collection():
    username = input("Username: ")
    pswd = getpass.getpass('Password:')
    client = pymongo.MongoClient("mongodb+srv://"+username+":"+pswd+"@nsp-cluster-zqniz.mongodb.net/test?retryWrites=true")
    game_records = client["NBA-Game-Data"]["Game-Records"]
    return game_records

def get_players_db():
    username = input("Username: ")
    pswd = getpass.getpass('Password:')
    client = pymongo.MongoClient("mongodb+srv://"+username+":"+pswd+"@nsp-cluster-zqniz.mongodb.net/test?retryWrites=true")
    players = client["Players"]
    return players

def get_team_last_5_full(collection, team_name, date):
    recs = collection.find(
        {"$and":[
            {
                "Date": {
                    "$lt": date
                }
            },
            {   "$or": [
                    {"Away.Name": team_name},
                    {"Home.Name": team_name}
                ]
            }
        ]}
    ).sort([("Date", pymongo.DESCENDING)]).limit(5)
    return recs

def get_team_last_5_reduced(collection, team_name, date):
    recs = collection.find(
        {"$and":[
            {
                "Date": {
                    "$lt": date
                }
            },
            {   "$or": [
                    {"Away.Name": team_name},
                    {"Home.Name": team_name}
                ]
            }
        ]}
    ).sort([("Date", pymongo.DESCENDING)]).limit(5)
    return [rec["Home"] if rec["Home"]["Name"]==team_name else rec["Away"] for rec in recs]

def get_player_last_5(db, player_name, date):
    recs = db['_'.join(player_name.split(' '))].find(
        {
            "Date": {
                "$lt": date
            }
        }
    ).sort([("Date", pymongo.DESCENDING)]).limit(5)
    return recs

if(__name__=='__main__'):
    main()