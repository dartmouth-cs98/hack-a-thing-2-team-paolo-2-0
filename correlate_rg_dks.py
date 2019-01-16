# Paolo Takagi-Atilano
# Hack A Thing 2
# Jan 15, 2019
# Script to prompt user to correct player name discrepancies between rotogrinder projections and draftkings scores
# Saves discrepancies into 'backtesting_data/sa_to_rg.json' for future use

import json
import os
import re
import requests
import sys
import time

import pandas as pd

from data import data

rgp = 'backtesting_data/{}/rotogrinders_predictions.csv'
dks = 'backtesting_data/{}/draftkings_actual_scores.csv'

js = {}
with open('backtesting_data/sa_to_rg.json') as f:
	js = json.loads(f.read())

for d in data:
	rg = pd.read_csv(rgp.format(d[0]), header=None)
	sa = {}
	with open(dks.format(d[0])) as f:
		sa = json.loads(f.read())

	print(d[0])
	print(sa)
	for p in rg[0].tolist():
		if p not in sa['fpts']:
			if p in js:
				if js[p] in sa['fpts']:
					sa['fpts'][p] = sa['fpts'][js[p]]
					del sa['fpts'][js[p]]
				else:
					del js[p]
			else:
				a = input('{} >> '.format(p)).split(';')
				if a[0] == '0':		# 0;fpts
					sa['fpts'][p] = float(a[1])
					print('adding')
				elif a[0] == '1':	# 1;sa_name
					try:
						sa['fpts'][p] = sa['fpts'][a[1]]
					except KeyError:
						with open('backtesting_data/sa_to_rg', 'w') as f:
							f.write(json.dumps(js))
					del sa['fpts'][a[1]]
					js[p] = a[1]
					print('switching')
				elif a[0] == '2':	# 2 (player didn't play)
					print('passing')
		
	with open(dks.format(d[0]), 'w') as f:
		f.write(json.dumps(sa))

	print()

with open('backtesting_data/sa_to_rg.json', 'w') as f:
	f.write(json.dumps(js))
