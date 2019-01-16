# Paolo Takagi-Atilano
# Hack A Thing 2
# Jan 15, 2019
# Script to scrape rotogrinders projections for date range in data.py

import json
import os
import re
import requests
import sys
import time

import pandas as pd

from datetime import datetime, timedelta
from data import data

roto_url = 'https://rotogrinders.com/projected-stats/nba-player?site=draftkings&date={}'
r = re.compile(r'data = .*;\n')

def get_rotogrinders(datestr):
	df = pd.DataFrame(columns=['player_name', 'salary', 'team', 'position', 'opp', 'ceil', 'floor', 'points'])
	a = r.search(requests.get(roto_url.format(datestr)).text)
	s = a.group(0)
	s = s[7:len(s)-2]

	js = json.loads(s)

	for i in range(len(js)):
		row = []
		row.append(js[i]['player_name'])
		row.append(int(float(js[i]['salary'])))
		row.append(js[i]['team'])
		row.append(js[i]['position'])
		row.append(js[i]['opp'])
		row.append(js[i]['ceil'])
		row.append(js[i]['floor'])
		row.append(js[i]['points'])

		df.loc[i] = row
	return df
	

base = 'backtesting_data/{}'
rgp = 'backtesting_data/{}/rotogrinders_predictions.csv'

for d in data:
	# date object
	date = datetime.strptime(d[0], '%d-%m-%Y')
	
	# rotogrinders datestr format
	datestr = date.strftime('%Y-%m-%d')

	# get projections and write them to csv
	df = get_rotogrinders(datestr)
	df.to_csv(rgp.format(d[0]), header=False, index=False)

	# sleeping to be polite
	time.sleep(1)
		
	# printing to show progress
	print(date)
