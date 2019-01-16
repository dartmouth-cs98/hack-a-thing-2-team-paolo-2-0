# Paolo Takagi-Atilano
# Hack A Thing 2
# Jan 15, 2019
# Script to scrape past draftkings player scores for date range in data.py
# Scrapes from SwishAnalytics.com

import json
import os
import re
import requests
import sys
import time

import pandas as pd

from datetime import datetime, timedelta
from data import data

dks_url = 'https://swishanalytics.com/optimus/nba/fanduel-draftkings-live-scoring?date={}'
r = re.compile(r'this\.players = .*;\n')

def get_dks(datestr):
	dks = {'fpts': {}}
	a = r.search(requests.get(dks_url.format(datestr)).text)
	s = a.group(0)
	s = s[15:len(s)-2]
	
	js = json.loads(s)

	for j in js:
		dks['fpts'][j['name']] = float(j['fpts'])

	return dks

dks = 'backtesting_data/{}/draftkings_actual_scores.csv'

for d in data:
	# date object
	date = datetime.strptime(d[0], '%d-%m-%Y')

	# SwishAnalytics datestr format
	datestr = date.strftime('%Y-%m-%d')

	# get projections and write them to json
	dk = get_dks(datestr)
	with open(dks.format(d[0]), 'w') as f:
		f.write(json.dumps(dk))

	# sleeping to be polite
	time.sleep(1)
	
	# printing to show progress	
	print(date)
	