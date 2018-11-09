import pymongo

def main():
    games = get_games_collection()
    players = get_players_collection()
    recs = get_all_games_on_date(games, "2017/10/17")
    recs2 = get_player_on_date(players, "LeBron James", "2017/10/17")
    for item in recs:
        print(item["Home"]["Name"] + " vs " + item["Away"]["Name"])
    for item2 in recs2:
        print(item2["Name"]+": "+str(item2["PTS"])+" points")

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
    recs = collection.find(
        {"$and":[
            {
                "Date": {
                    "$lt": date
                }
            },
            {
                "Name": {
                    "$eq": player_name
                }
            }
        ]}
    ).sort([("Date", pymongo.DESCENDING)]).limit(5)
    return recs

def get_player_on_date(collection, player_name, date):
    recs = collection.find(
        {"$and":[
            {
                "Date": {
                    "$eq": date
                }
            },
            {
                "Name": {
                    "$eq": player_name
                }
            }
        ]}
    )
    return recs

if(__name__=='__main__'):
    main()