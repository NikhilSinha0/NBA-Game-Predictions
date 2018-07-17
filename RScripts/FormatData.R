## Format Data to work with

####################################################################
## Can run every time or just save data into a workspace and load that everytime
library(mongolite)
mongo<- mongo(collection = "Game-Records", db = "NBA-Game-Data", url = "mongodb+srv://nsp_summer_admin:FightOn2018@nsp-cluster-zqniz.mongodb.net/test?retryWrites=true", verbose = TRUE)


# find all games played in 2007
nba <- mongo$find('{ "Date" : { "$regex" : "2007.*", "$options" : "i" }  }')

# Save workspace as NBA_2007

####################################################################

# load data (keeps data but loses mongo connection)
load("~/R/NBA_2007.RData")

#install.packages("data.table")
library(data.table)

# Extract Player Data
AwayPlayers <- nba$Away$Players
HomePlayers <- nba$Home$Players

# Format Player Data as Data Table
AwayPlayers <- data.table(AwayPlayers)
HomePlayers <- data.table(HomePlayers)

####################################################################

# Extract Data for one team for one game
# data <- DataTable[[column]][[row]][row in list, column in list]

# Example 1 - extracts data for all POR players in first away game of season
POR <- AwayPlayers[[1]][[1]][]

# Example 2 - extracts data for Carlos Boozer in first away Jazz game
Boozer <- AwayPlayers[[1]][[2]][2,]

