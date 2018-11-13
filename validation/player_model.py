




def player_model(player_model_input):
    player_model_output = {}
    player_model_output['Home'] = player_model_input['Home']
    player_model_output['Away'] = player_model_input['Away']

    return player_model_output



def get_player_model_input(game):
    player_model_input = {}

    player_model_input['Home'] = {}
    player_model_input['Away'] = {}
    player_model_input['Date'] = game['Date']

    home_player_list = game['Home']['Players']
    away_player_list = game['Away']['Players']

    # for each player in home:
        #
        # ***
    # for each player in away:
        # ***
    return player_model_input



def main(game):
    player_model_input = get_player_model_input(game)
    player_model_output = player_model(player_model_input)
    # print("Player Model Main")
