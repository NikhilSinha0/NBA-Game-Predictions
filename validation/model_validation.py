
# import player_model
# import team_model
# import prediction_model

import json
from pprint import pprint

"""
Inputs:
1) Player Scores
2) Team Scores
3) Auxillary Data


Outputs:
1) Game Outcome for Home Team (Binary, 1 = Win, 0 = Lose)

"""




def get_games(start_date, end_date):
    with open('sample_game.json') as f:
        games = json.load(f)
    return games


def get_player_scores(home_player_data, away_player_data):
    player_scores = 0
    return player_scores


def get_team_scores(home_team_data, away_team_data):
    team_scores = 0
    return team_scores


def player_model(players_scores):
    player_game_scores = 0
    return player_game_scores


def team_model(team_scores):
    team_game_scores = 0
    return team_game_scores


def get_aux_data(game):
    aux_data = 0
    return aux_data



def prediction_model(player_game_scores, team_game_scores, aux_data):
    prediction = 1

    return prediction



def predict(start_date, end_date):

    games = get_games(start_date, end_date)

    # intitialize model inputs
    player_scores = {}
    player_game_scores = {}

    team_scores = {}
    team_game_scores = {}

    aux_data = {}

    # intitialize accuracy and validation outputs
    model_accuracy = {}
    model_accuracy['total'] = 0
    model_accuracy['correct'] = 0
    model_accuracy['incorrect'] = 0

    validation_output = []


    # run prediction model on given game set with accuracy statistics

    for game in games:
        output = {}
        model_accuracy['total'] +=1

        target = game['Home']['Win']


        home_player_data = game['Home']['Players']
        away_player_data = game['Away']['Players']

        home_team_data = game['Home']['Team Totals']
        away_team_data = game['Away']['Team Totals']


        player_scores = get_player_scores(home_player_data, away_player_data)
        team_scores = get_team_scores(home_team_data, away_team_data)

        player_game_scores = player_model(player_scores)
        team_game_scores = team_model(team_scores)

        aux_data = get_aux_data(game)

        result = prediction_model(player_game_scores, team_game_scores, aux_data)

        output['Home_Team'] = game['Home']['Name']
        output['Away_Team'] = game['Away']['Name']
        output['Date'] = game['Date']
        output['Prediction'] = result
        output['Actual'] = target

        if result == target:
            model_accuracy['correct'] += 1
        else:
            model_accuracy['incorrect'] += 1

        validation_output.append(output)

    return validation_output, model_accuracy

start_date = 0
end_date = 0
result = predict(start_date, end_date)
print(result)
