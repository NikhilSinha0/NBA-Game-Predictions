import pymongo

def main():
    games = get_games_collection()
    players = get_players_collection()
    recs = get_all_games_on_date(games, "2017/10/17")
    recs2 = get_player_on_date(players, "LeBron James", "2017/10/17")
    recs3 = get_distinct_train_names(players)
    recs4 = get_partial_batch(players, "Brandon Ingram")
    for item in recs:
        print(item["Home"]["Name"] + " vs " + item["Away"]["Name"])
    for item2 in recs2:
        print(item2["Name"]+": "+str(item2["PTS"])+" points")
    print(len(recs3))
    print(list(recs4[0].values()))

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

def get_distinct_train_names(collection):
    names = collection.find({"Date": {"$lt": "2017/10/16"}}).distinct("Name")
    return names

def get_distinct_test_names(collection):
    names = collection.find({"Date": {"$gt": "2017/10/16"}}).distinct("Name")
    return names

def get_distinct_team_train_names(collection):
    names = collection.find({"Date": {"$lt": "2017/10/16"}}).distinct("Home.Name")
    return names

def get_distinct_team_test_names(collection):
    names = collection.find({"Date": {"$gt": "2017/10/16"}}).distinct("Home.Name")
    return names

def get_partial_batch(collection, pname):
    recs = collection.find(
        {"$and":[
            {
                "Date": {
                    "$lt": "2017/10/16"
                }
            },
            {
                "Name": {
                    "$eq": pname
                }
            },
            {
                "MP": {
                    "$type": 1 #Skips DNPs
                }
            }
        ]}
    ).sort([("Date", pymongo.ASCENDING)])
    return list(recs)

def get_team_batch(collection, team_name):
    recs = collection.find(
        {"$and":[
            {
                "Date": {
                    "$lt": "2017/10/16"
                }
            },
            {   "$or": [
                    {"Away.Name": team_name},
                    {"Home.Name": team_name}
                ]
            }
        ]}
    ).sort([("Date", pymongo.ASCENDING)])
    return list(recs)

def get_team_home_batch(collection, team_name):
    recs = collection.find(
        {"$and":[
            {
                "Date": {
                    "$lt": "2017/10/16"
                }
            },
            {
                "Home.Name": {
                    "$eq": team_name
                }
            }
        ]}
    ).sort([("Date", pymongo.ASCENDING)])
    return list(recs)

def get_partial_test(collection, pname):
    recs = collection.find(
        {"$and":[
            {
                "Date": {
                    "$gt": "2017/10/16"
                }
            },
            {
                "Name": {
                    "$eq": pname
                }
            },
            {
                "MP": {
                    "$type": 1 #Skips DNPs
                }
            }
        ]}
    ).sort([("Date", pymongo.ASCENDING)])
    return list(recs)

def get_team_test(collection, team_name):
    recs = collection.find(
        {"$and":[
            {
                "Date": {
                    "$gt": "2017/10/16"
                }
            },
            {   "$or": [
                    {"Away.Name": team_name},
                    {"Home.Name": team_name}
                ]
            }
        ]}
    ).sort([("Date", pymongo.ASCENDING)])
    return list(recs)

def get_team_home_test(collection, team_name):
    recs = collection.find(
        {"$and":[
            {
                "Date": {
                    "$gt": "2017/10/16"
                }
            },
            {
                "Home.Name": {
                    "$eq": team_name
                }
            }
        ]}
    ).sort([("Date", pymongo.ASCENDING)])
    return list(recs)

if(__name__=='__main__'):
    main()
