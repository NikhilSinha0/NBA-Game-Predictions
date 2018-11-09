import pymongo

def main():
    client = pymongo.MongoClient("mongodb+srv://public:bO4kawu45n4yEaD7@nsp-cluster-zqniz.mongodb.net/test?retryWrites=true")
    game_records = client["NBA-Game-Data"]["Game-Records"]
    recs = game_records.find(
        {
            "Date": {
                "$eq": "2017/10/30"
            }
        }
    ).sort([("Date", pymongo.DESCENDING)]).limit(5)
    for item in recs:
        print(item["Home"]["Name"] + " vs " + item["Away"]["Name"])

def get_games_collection():
    client = pymongo.MongoClient("mongodb+srv://public:bO4kawu45n4yEaD7@nsp-cluster-zqniz.mongodb.net/test?retryWrites=true")
    game_records = client["NBA-Game-Data"]["Game-Records"]
    return game_records

def get_players_collection():
    client = pymongo.MongoClient("mongodb+srv://public:bO4kawu45n4yEaD7@nsp-cluster-zqniz.mongodb.net/test?retryWrites=true")
    players = client["Players"]["Players"]
    return players

def get_team_game_on_date(collection, team_name, date):
    recs = collection.find(
        {"$and":[
            {
                "Date": {
                    "$eq": date
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

def get_all_games_on_date(collection, date):
    recs = collection.find(
        {
            "Date": {
                "$eq": date
            }
        }
    ).sort([("Date", pymongo.DESCENDING)]).limit(5)
    return recs

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

def get_player_last_5(collection, player_name, date):
    name = '_'.join(player_name.split(' '))
    collection.find(
        {"$and":[
            {
                "Date": {
                    "$lt": date
                }
            },
            {
                "Name": {
                    "$eq": name
                }
            }
        ]}
    ).sort([("Date", pymongo.DESCENDING)]).limit(5)
    return recs

if(__name__=='__main__'):
    main()