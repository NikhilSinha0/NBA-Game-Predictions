# Summer_Project

Command to run the crawler in /crawler is "./run_crawler.bat"

Make sure to first install dependencies using the command "pip install -r requirements.txt"

IMPORTANT: This crawler will take a while because we play nicely with basketball-reference.com's robots.txt policy. The policy asks us to take a 3 second break between each time we access a page on the site, so getting a year's worth of games will take around 1.5 hours. However, this is not a compute-heavy program, so you can start it and go do other things while it gets the data for you. We output a csv file (if you want to look at the data for a game) and a JSON file (if you want to import the data into a database or program) for each game, put in separate folders (game_csvs and game_jsons).

Distances between stadiums calculated using the code at http://andrew.hedges.name/experiments/haversine/
