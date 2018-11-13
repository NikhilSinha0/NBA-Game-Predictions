# import model_validation
# import prediction_model
import argparse
import sys
sys.path.append('../crawler')
print(sys.path)
from crawler import main as main2
# from application.app.folder.file import func_name
# from .. import crawler.main
import importlib
import json
# from data_loader import get_team_last_5_full
# from data_loader import get_team_last_5_reduced
# from data_loader import get_player_last_5

import get_aux_data

from player_model_validation import player_model_validation
from team_model_validation import team_model_validation
import prediction_model_validation

# from player_model_validation import get_player_score_labels


"""
Given a specified:
1. Player model file name
2. team model file name
3. Prediction model file name
4. Boolean 'yesterday'

Run data loader (what are inputs and outputs?)
	Input: Start Date
	Output: End Date
	(if 'Yesterday', )

Run Prediction Model on returned test set and return accuracy statistics

"""



def main():
	print()

	# print(sys.argv[1:])
	# GET MODEL FILENAMES FROM COMMAND LINE
	argparser = argparse.ArgumentParser()
	argparser.add_argument('player_model',help='')
	argparser.add_argument('team_model',help='')
	argparser.add_argument('prediction_model',help='')
	argparser.add_argument('yesterday',help='')



	args = argparser.parse_args()
	player_model = args.player_model
	team_model = args.team_model
	prediction_model = args.prediction_model
	yesterday = args.yesterday

    # taking full .py filename as input from commandline, indexing out the '.py' for importing
	player_model = importlib.import_module(args.player_model[:-3])
	team_model = importlib.import_module(args.team_model[:-3])
	prediction_model = importlib.import_module(args.prediction_model[:-3])

	collection = ""
	team_name = ""
	date = ""

	with open('sample_game.json') as json_data:
		data = json.load(json_data)

	if yesterday == False:
		print('False')

		input_games = data
	else:
		print('True')
		# input_games = get_yesterday(collection, team_name, date)
		input_games = data


	player_game_scores = {}
	team_scores = {}
	team_game_scores = {}


	actual_player_scores = []
	actual_team_scores = []
	actual_game_outcomes = []


	# actual_player_scores = player_score_calculator(input_games)
	# actual_team_scores = team_score_calculator(input_games)
	actual_game_outcomes = prediction_model_validation.get_actual_game_outcomes(input_games)
	#

	prediction_model_output = []
	for game in input_games:

		output = {}
		output['Home'] = game['Home']['Name']
		output['Away'] = game['Away']['Name']
		output['Date'] = game['Date']

    	# intitialize prediction model inputs
		aux_data = {}
		player_model_output = {}
		team_model_output = {}

		# get inputs for final prediction model
		player_model_result = player_model.main(game)
		team_model_result = team_model.main(game)
		aux_data = get_aux_data.main(game)

		# run prediction model on given game with accuracy statistics

		# output['Player Predictions'] = player_model_result
		# output['Team Predictions'] = team_model_result
		output['Prediction'] = prediction_model.main(player_model_result,team_model_result, aux_data)
		prediction_model_output.append(output)


    # player_model_validation = player_model_validation(player_model_output, actual_player_scores)
    # team_model_validation = team_model_validation(team_model_output, actual_team_scores)
	# print(actual_game_outcomes)

	prediction_model_validation.main(prediction_model_output, actual_game_outcomes)

	# player_model_descriptive= player_model_descriptive(player_model_output, actual_player_scores)
    # team_model_descriptive = team_model_descriptive(team_model_output, actual_team_scores)
    # prediction_model_descriptive = prediction_model_descriptive(prediction_model_ouput, actual_game_outcomes)




main()
