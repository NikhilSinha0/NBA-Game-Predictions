import pandas as pd
# import data_loader.basic_import as basic_import
# from data_loader.main import get_all_games_on_date
import sys
sys.path.insert(0, '../data_loader/')
import loader
import random
from datetime import datetime

"""
Inputs:
1) All games in database

Outputs:
1) Top level ['.txt'] file with [300 dates] that will be left for validation

"""


def get_dates_with_games():

    date_list = []
    start_date = '2007/05/03'
    end_date = '2017/12/31'

    date_list = pd.date_range(start_date, end_date).tolist()

    collection = loader.get_games_collection()
    dates_with_games = []
    # dates_with_games = ['2007-05-03','2011-05-10','2007-05-03','2011-05-10','2007-05-03','2011-05-10','2007-05-03','2011-05-10','2007-05-03','2011-05-10']

    # Get game objects from Mongo
    # date = '2017/10/17'
    # games = list(loader.get_all_games_on_date(collection, date))
    # print(games)

    for date in date_list:
        date = str(date.date())
        formated_date = date.replace('-','/')
        games = list(loader.get_all_games_on_date(collection, formated_date))
        # print(formated_date)
        # print(len(games))
        if (len(games) > 0):
            dates_with_games.append(formated_date)

    return dates_with_games



def get_test_dates(game_date_list):
    test_dates = []
    test_sample_size = 0.2
    num_test_dates = int(test_sample_size * float(len(game_date_list)))
    #generate list of 'num_test_dates' many random numbers
    random_numbers = random.sample(range(0, len(game_date_list)), num_test_dates)
    for number in  random_numbers:
        test_date = game_date_list[number]
        test_dates.append(test_date)
    return test_dates


def main():
    game_date_list = get_dates_with_games()
    test_dates = get_test_dates(game_date_list)

    # Output test games to top level .txt file
    with open('../test_dates.txt', 'a') as f:
        f.write("%s\n" % test_dates)


if(__name__=='__main__'):
    main()
