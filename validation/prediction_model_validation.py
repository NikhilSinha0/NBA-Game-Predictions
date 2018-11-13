
import pandas as pd


#
# prediction_model_output = [
#     {
#         "Home":"<Home Team 1>",
#         "Away":"<Away Team 1>",
#         "Date":"<Date 1>",
#         "Prediction": 0
#     },
#     {
#         "Home":"<Home Team 2>",
#         "Away":"<Away Team 2>",
#         "Date":"<Date 2>",
#         "Prediction": 1
#     },
# ]
#
# actual_game_outcomes = [
#     {
#         "Home":"<Home Team 1>",
#         "Away":"<Away Team 1>",
#         "Date":"<Date 1>",
#         "Actual": 0
#     },
#     {
#         "Home":"<Home Team 2>",
#         "Away":"<Away Team 2>",
#         "Date":"<Date 2>",
#         "Actual": 0
#     },
# ]


def get_actual_game_outcomes(input_games):
    actual_game_outcomes = [{}]

    for game in input_games:
        game_outcome = {}
        game_outcome['Home'] = game['Home']['Name']
        game_outcome['Away'] = game['Away']['Name']
        game_outcome['Date'] = game['Date']
        game_outcome['Actual'] = game['Home']['Win']

        actual_game_outcomes.append(game_outcome)

    return actual_game_outcomes


def get_prediction_model_validation_input(prediction_model_output, actual_game_outcomes):

    prediction_model_output_df = pd.DataFrame(columns=['Home','Away','Date','Prediction'])
    actual_game_outcomes_df = pd.DataFrame(columns=['Home','Away','Date','Actual'])
    # create two data frames out of dictionaries
    for output in prediction_model_output:
        new_row = pd.DataFrame(output,columns=['Home','Away','Date','Prediction'], index=[0])
        prediction_model_output_df = pd.concat([prediction_model_output_df, new_row], ignore_index=True)


    for output in actual_game_outcomes:
        new_row = pd.DataFrame(output,columns=['Home','Away','Date','Actual'], index=[0])
        actual_game_outcomes_df = pd.concat([actual_game_outcomes_df, new_row], ignore_index=True)

    # append actual game score to prediction_model_output
    # (merge on Home team and Date),
    prediction_model_validation_input_df = pd.merge(prediction_model_output_df, actual_game_outcomes_df, how='left', on=['Home','Away','Date'])

    return prediction_model_validation_input_df




def prediction_model_validation(prediction_model_validation_input_df):
    # intitialize accuracy and validation outputs

    model_accuracy = {}
    model_accuracy['total'] = 0
    model_accuracy['correct'] = 0
    model_accuracy['incorrect'] = 0


    # for each row in data frame, calculate
    for index, row in prediction_model_validation_input_df.iterrows():
        model_accuracy['total'] += 1

        if row['Prediction'] == row['Actual']:
            model_accuracy['correct'] += 1
        else:
            model_accuracy['incorrect'] += 1


    return model_accuracy



def main(prediction_model_output, actual_game_outcomes):
    prediction_model_validation_input_df = get_prediction_model_validation_input(prediction_model_output, actual_game_outcomes)
    model_accuracy = prediction_model_validation(prediction_model_validation_input_df)
    print(prediction_model_validation_input_df)
    print(model_accuracy)
