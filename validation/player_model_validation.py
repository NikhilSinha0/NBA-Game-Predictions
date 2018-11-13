import json

"""
3 Model Validation Functions:
    1) Player Model Validation
        For each Player:
            Actual PLayer Score
            Predicted PLayer Score
        Average Player Score Prediction Error
        Max Player Score Prediction Error
        Min Player Score Prediction Error
        Player Score Prediction Variance

    2) Team Model Validation
    3) Prediction Model Validation
        Total number of correct predictions
        For all correct predictions:
            ** Summary/Descriptive Statistics **
            Prediction Accuracy by team
            Feature Prevalance


"""

player_model_output = {
    "Model_Name":"<File name>",
    "Date":"<DATE>",
    "Name":"<Team Name>",
    "Player_Scores":{
        "Player_Name":60,
        "Player_Name":70,
    }
}

actual_player_scores = {
    "Date":"<DATE>",
    "":"<>",
    "Name":"<Team Name>",
    "Player_Scores":{
        "Player_Name":60,
        "Player_Name":70,
    }
}


def get_player_scores(player_list):
    player_scores = {}
    for player_stats in player_list:

        player_name = player_stats['Name']
        points_scored = float(player_stats['PTS'])
        field_goals = float(player_stats['FG'])
        field_goal_attempts = float(player_stats['FGA'])
        free_throw_attempts = float(player_stats['FTA'])
        free_throws = float(player_stats['FT'])
        offensive_rebounds = float(player_stats['ORB'])
        defensive_rebounds = float(player_stats['DRB'])
        steals = float(player_stats['STL'])
        assists = float(player_stats['AST'])
        blocks = float(player_stats['BLK'])
        personal_fouls = float(player_stats['PF'])
        turnovers = float(player_stats['TOV'])

        game_score = (points_scored + (0.4 * field_goals) - (0.7 * field_goal_attempts) - (0.4 * (free_throw_attempts - free_throws)) + (0.7 * offensive_rebounds) + (0.3 * defensive_rebounds) + steals + (0.7 * assists) + (0.7 * blocks) - (0.4 * personal_fouls) - turnovers)
        player_scores[player_name] = game_score

    return player_scores




def get_player_score_labels(input_games):
    player_score_labels = []

    for game in input_games:

        player_scores = {}
        player_scores['Home'] = {}
        player_scores['Away'] = {}
        player_scores['Date'] = game['Date']

        home_player_list = game['Home']['Players']
        away_player_list = game['Away']['Players']

        player_scores['Home'] = get_player_scores(home_player_list)
        player_scores['Away'] = get_player_scores(away_player_list)

        # append player scores to output
        player_score_labels.append(player_scores)

    return player_score_labels



def get_player_model_validation_input_df(player_model_output, actual_player_scores):
    player_model_validation_input_df = {}


    # create two data frames out of dictionaries
    player_model_output_df = pd.DataFrame(columns=['Home','Away','Date','isHome','Name','Predicted'])
    actual_player_scores_df = pd.DataFrame(columns=['Home','Away','Date','isHome','Name','Actual'])
    # create two data frames out of dictionaries
    for output in prediction_model_output:
        new_row = pd.DataFrame(output,columns=['Home','Away','Date','isHome','Name','Predicted'], index=[0])
        player_model_output_df = pd.concat([player_model_output_df, new_row], ignore_index=True)


    for output in actual_game_outcomes:
        new_row = pd.DataFrame(output,columns=['Home','Away','Date','isHome','Name','Actual'], index=[0])
        actual_player_scores_df = pd.concat([actual_player_scores_df, new_row], ignore_index=True)

    # append actual game score to player_model_output
    # (merge on Home team and Date),
    player_model_validation_input_df = pd.merge(player_model_output_df, actual_player_scores_df, how='left', on=['Home','Away','Date','Name'])

    return player_model_validation_input_df





def player_model_validation(player_model_validation_input):
    validation_output = {}
    return validation_output



###### HARD CODED JSON INPUT ######
with open('sample_game.json') as json_data:
    sample_games = json.load(json_data)
# player_list = sample_games[0]['Away']['Players']


labels = get_player_score_labels(sample_games)
print(labels)
