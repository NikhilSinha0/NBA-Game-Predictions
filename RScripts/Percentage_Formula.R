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
percent <- transmute(nba,
                     Player = Player,
                     Tm = Tm,
                     G = G,
                     MP = MP,
                     FG. = FG. * 100,
                     X3P. = X3P. * 100,
                     X2P. = X2P. * 100,
                     eFG. = eFG. * 100,
                     FT. = FT. * 100,
                     TS. = TS. * 100,
                     ORB. = ORB.,
                     DRB. = DRB.,
                     AST. = AST.,
                     STL. = STL.,
                     BLK. = BLK.,
                     TOV. = TOV.,
                     USG. = USG.)

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

#########################################################
## Sum all percentages with correct scaling

percent <- mutate(percent, PlayerScore = rowSums(percent[,c('FG.', 'X3P.', 'X2P.', 'eFG.', 'FT.',  'TS.', 'ORB.', 'DRB.', 'AST.', 'STL.', 'BLK.', 'TOV.', 'USG.')], na.rm = TRUE))
percent <- mutate(percent, PScore = PlayerScore * MP / 48)
percent <- mutate(percent, PS.game = PScore * G / 82)

## Order by top player score per minute
percent <- arrange(percent, desc(PScore))

## Group players by team
team <- group_by(percent, Tm)

## Sum player data into raw team score
ts <- summarise(team, TeamScore = sum(PS.game, na.rm = TRUE))
ts <- arrange(ts, desc(TeamScore))

## needs work but scaling by game helps team score


#########################################################
## Create arbitrary factors

adjusted <- transmute(percent,
                      Player = Player,
                      Tm = Tm,
                      G = G,
                      MP = MP,
                      eFG. = 0.25 * eFG. ,
                      ORB. = 0.8 * ORB. ,
                      DRB. = 0.5 * DRB. ,
                      AST. = 0.33 * AST. ,
                      STL. = 2 * STL. ,
                      BLK. = 2 * BLK. ,
                      TOV. = -0.75 * TOV.,
                      USG. = 0.5 * USG. )

adjusted <- mutate(adjusted, PlayerScore = rowSums(percent[,c('eFG.', 'FT.', 'ORB.', 'DRB.', 'AST.', 'STL.', 'BLK.', 'TOV.', 'USG.')], na.rm = TRUE))
adjusted <- mutate(adjusted, PScore = PlayerScore * MP / 48)
adjusted <- mutate(adjusted, PS.game = PScore * G / 82)

## Order by top player score per minute
adjusted <- arrange(adjusted, desc(PScore))

## Group players by team
team1 <- group_by(adjusted, Tm)

## Sum player data into raw team score
ts1 <- summarise(team1, TeamScore = mean(PS.game, na.rm = TRUE))
ts1 <- arrange(ts1, desc(TeamScore))

## scalings are not good - look into running monte carlo for scale factors
