library("mongolite")
m<- mongo(collection = "Game-Records", db = "NBA-Game-Data", url = "mongodb+srv://nsp_summer_admin:FightOn2018@nsp-cluster-zqniz.mongodb.net/test?retryWrites=true", verbose = TRUE)
matt <- m$aggregate('[
  {"$match": {
    "$or": [
      {"Home.Players.Name": "Matt Barnes"}, 
      {"Away.Players.Name": "Matt Barnes"}
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
  }]')