#Bobby Crawford - CS 98 Hackathing 2

#import all necessary modules
import json
import multiprocessing
import pandas as pd

from data import data
from solver import solve

# configs are tuples: (num_lineups, overlap, player_csv, team_csv, actual_csv, name)
def backtest_fast(configs):
	processes = []
	scores_list = []
	for i in range(len(configs)):
		scores = multiprocessing.Array('d', configs[i][0])
		scores_list.append(scores)
		processes.append(multiprocessing.Process(target=backtest_fast_helper,
			args=(configs[i], scores)))

    #start all processes
	for process in processes:
		process.start()

    #join all processes
	for process in processes:
		process.join()

    #create initial dataframe
	df = pd.DataFrame()
	for i in range(len(scores_list)):
		df[configs[i][5]] = pd.Series(scores_list[i][:])
	return df

# helper function for faster multiprocessing solution
def backtest_fast_helper(config, scores):
	lineups = solve(config[0], config[1], config[2], config[3])

	with open(config[4], 'r') as f:
		actuals = json.loads(f.read())['fpts']

	# adding actual score to every single lineup
	for i in range(len(lineups)):
		scores[i] = sum([actuals[player] for player in lineups[i]['Name'].tolist() if player in actuals])

base = 'backtesting_data/{}/{}'

# setting up all the proper configs from data list
configs = []
for d in data:
	config = (100, 7,
		base.format(d[0], 'rotogrinders_predictions.csv'),
		base.format(d[0], d[1]),
		base.format(d[0], 'draftkings_actual_scores.csv'),
		'{};{}'.format(d[0], d[1]))
	configs.append(config)

# write results to csv
backtest_fast(configs).to_csv('results.csv')
