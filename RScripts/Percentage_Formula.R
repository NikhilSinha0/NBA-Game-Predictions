## Percentage Formula

#########################################################
## Set up data

## clear workspace
rm(list=ls())

## set working directory (change to personal wd)
setwd("~/R/NBA_Summer_Project")

## load in data
nba <- read.csv("NBA_17_18.csv")
nba$Rk <- NULL

#install.packages("dplyr")
# intro to package https://cran.r-project.org/web/packages/dplyr/vignettes/dplyr.html
library(dplyr)

## convert to tibble (different version of data frame)
nba <- as_tibble(nba)

## change all percentages to be out of 100
##nba$FG. <- nba$FG. * 100
##nba$X3P. <- X3P. * 100

#########################################################
## Create Player Score

## create player score (sum all) and also per minute player score
nba <- mutate(nba, PlayerScore = rowSums(nba[,c('FG.', 'X3P.', 'X2P.', 'eFG.', 'FT.',  'TS.', 'ORB.', 'DRB.', 'AST.', 'STL.', 'BLK.', 'TOV.', 'USG.')], na.rm = TRUE))
nba <- mutate(nba, PScore = PlayerScore * MP / 48)

## Order by top player score per minute
nba <- arrange(nba, desc(PScore))

## Group players by team
team <- group_by(nba, Tm)

## Sum player data into raw team score
ts <- summarise(team, TeamScore = sum(PScore, na.rm = TRUE))
ts <- arrange(ts, desc(TeamScore))
## absolutely awful but a good way to test out functions






