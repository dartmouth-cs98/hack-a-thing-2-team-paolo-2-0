#Bobby Crawford - CS 98 Hackathing 2

#import all necessary modules
import json

import numpy as np
import pandas as pd

# evaluate general effectiveness of our results
def eval():
	df = pd.read_csv('results.csv') #generates initial dataframe from results.csv
	cash, gpp = get_lines(df)
	cols = list(df)
	cashes = 0
	gpps = 0
	gpp_11x = 0
	gpp_12x = 0
	gpp_13x = 0
	totc = 0
	totg = 0
	suptot = 0

	for i in range(1, len(cols)):
		if not np.isnan(cash[i]):
			cashes += len([a for a in df[df.columns[i]].tolist() if a > cash[i]])
			totc += len([a for a in df[df.columns[i]].tolist() if a > 100])


		if not np.isnan(gpp[i]):
			gpps += len([a for a in df[df.columns[i]].tolist() if a > gpp[i]])
			gpp_11x += len([a for a in df[df.columns[i]].tolist() if a > gpp[i]*1.1])
			gpp_12x += len([a for a in df[df.columns[i]].tolist() if a > gpp[i]*1.2])
			gpp_13x += len([a for a in df[df.columns[i]].tolist() if a > gpp[i]*1.3])
			totg += len([a for a in df[df.columns[i]].tolist() if a > 100])

		suptot += len([a for a in df[df.columns[i]].tolist()])

	fcash = (cashes/totc)*100 if (cashes != 0 and totc != 0) else np.nan
	fgpp = (gpps/totg)*100 if (gpps != 0 and totg != 0) else np.nan
	fgpp_11x = (gpp_11x/totg)*100 if (gpps != 0 and totg != 0) else np.nan
	fgpp_12x = (gpp_12x/totg)*100 if (gpps != 0 and totg != 0) else np.nan
	fgpp_13x = (gpp_13x/totg)*100 if (gpps != 0 and totg != 0) else np.nan
	ftot = totg if totg != 0 else np.nan


	if not np.isnan(fcash):
		print('> Cash Line: {}'.format(fcash))
	if not np.isnan(fgpp):
		print('> Gpp Line: {}'.format(fgpp))
	if not np.isnan(fgpp_11x):
		print('> Gpp Line*1.1: {}'.format(fgpp_11x))
	if not np.isnan(fgpp_12x):
		print('> Gpp Line*1.2: {}'.format(fgpp_12x))
	if not np.isnan(fgpp_13x):
		print('> Gpp Line*1.3: {}'.format(fgpp_13x))

#retrieve lineups
def get_lines(df):
	cash = ['cash']
	gpp = ['gpp']
	cols = list(df)
	for i in range(1, len(cols)):
		info = cols[i].split(';')
		info[1] = info[1].replace('teams_', '').replace('.csv', '')

		js = json.loads(open('backtesting_data/{}/cash_stats.json'.format(info[0])).read())[info[1]]

		if 'cash' in js:
			cash.append(js['cash'])
		else:
			cash.append(np.nan)

		if 'gpp' in js:
			gpp.append(js['gpp'])
		else:
			gpp.append(np.nan)

	return cash, gpp

#ultimately evaluate lineups
eval()
