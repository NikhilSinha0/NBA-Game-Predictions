import pymongo
import getpass

def main():
    username = input("Username: ")
    pswd = getpass.getpass('Password:')
    client = pymongo.MongoClient("mongodb+srv://"+username+":"+pswd+"@nsp-cluster-zqniz.mongodb.net/test?retryWrites=true")
    collection = client["NBA-Game-Data"]["Game-Records"]
    matt_barnes = collection.aggregate([
    {"$match": {
        "$or": [
            {'Home.Players.Name': 'Matt Barnes'}, 
            {'Away.Players.Name': 'Matt Barnes'}
        ]
    }}, 
    {"$project": {
        "Home.Players": {
            "$filter": {
                "input": "$Home.Players", 
                "as": "hplayers", 
                "cond": {
                    "$eq": ["$$hplayers.Name", "Matt Barnes"]
                }
            }
        },
        "Away.Players": {
            "$filter": {
                "input": "$Away.Players", 
                "as": "hplayers", 
                "cond": {
                    "$eq": ["$$hplayers.Name", "Matt Barnes"]
                }
            }
        }  
    }  
    }])
    for matt_barnes:
        print(doc)

if(__name__=='__main__'):
    main()