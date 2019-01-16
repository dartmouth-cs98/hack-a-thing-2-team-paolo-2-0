# Hack A Thing 2: DraftKings Backtesting
## Paolo Takagi-Atilano and Bobby Crawford

**What we made:**

We realized that there was a flaw in our first Hack A Thing.  We don't know how well our lineups perform unless we spend a lot of money on them.  As such, for our second Hack A Thing, we set up backtesting infrastructure so that we could test our strategy on past DraftKings competitions.

**Scraping, Correlating, and Collecting:**

First, we had to collect the necessary data for backtesting.  Paolo did this.  For each past competition, four components had to be collected:  the `rotogrinders_predictions.csv`, `draftkings_actual_scores.csv`, `teams.csv`, and `cash_stats.json`.  Also first Paolo created `data.py`, which just as a list (called `data`), which is a tuple of every date and `teams.csv` for each competition. `rotogrinders_predictions.csv` are the rotogrinders player projections for that particular day.  These were scraped by the `scrape_roto_past.py` script.  `draftkings_actual_scores.csv` maps the each player's name to the number of fantasy points that they scored for that particular competition.  These were scraped by the `scrape_dk_actuals.py`, which works quite similarly to the `scrape_roto_past.py` script.  These scores were scraped from `swishanalytics.com` because it is easier to scrape than DraftKings, and to comply with DraftKings not wanting their site to be scraped.  `teams.csv` is the list of valid teams for that particular competition.  We could not find a way to scrape this automatically, so each of these files was collected manually.  `cash_stats.json` shows the average scores needed to "cash" in different competitions for a given time, for both "cash competitions" (all winners get the same amount), and "tournament competitions" (winners get more the better they score).  Again, we could find a way to scrape this, so it was also collected manually.

Finally, an issue arose in that there were discrepancies between the actual scores scrated from swish and the projections scraped from rotogrinders.  Some players were missing from the swish actual scores, and some had different names on each site (i.e. Larry Nance" and "Larry Nance Jr.").  To correct this, Paolo wrote a script called `correlate_rg_dks.py`, which prompted to user to correct the discrepancies by either changing the name or adding the entry (which they had to find manually on DraftKings).  Name switches were saved in `sa_to_rg.json` for future use.  An easy way to check for discrepancies is by running this script and making sure you are never prompted to make any corrections.  At this point, all the necessary data was collected to conduct backtesting.  All this data is included in the git repo for reference.

**Backtesting:**

Next was implementing the actual backtesting itself.  Bobby did this.  For each element in the list in `data.py`, he used the `solve` method from `solver.py` that was written for Hack A Thing 1 to generate 100 lineups.  Then he calculated the score the lineup actually got based on the corresponding `draftkings_actual_scores.csv` file.  Then every score for lineup for every competition was saved to a single `results.csv` file (included in git repo for reference).  Thus the backtesting was completed.  Finally was to evaluate how the lineups did.  This was all done in the `backtest.py` script.  We used multiprocessing so that each competition could be solved at the same time, thouroughly speeding up our wait time for the file.

**Evaluating:**

Now that we have created the `results.csv` file, last we compared it to the `cash_stats.json` files to get a general sense on how our model performed.  Bobby did this as well in the `eval_results.py` script.  For each competition, it tallied five numbers: 

* The number of lineups above the cash line
* The number of lineups above the tournament line
* The number of lineups above the (tournament line * 1.1)
* The number of lineups above the (tournament line * 1.2)
* The number of lineups above the (tournament line * 1.3)

It then aggregated these results accross all competitions, and outputted the final numbers as percentages.  Here is the output that we got:

`> Cash Line: 49.8`

`> Gpp Line: 34.6551724137931`

`> Gpp Line*1.1: 9.310344827586208`

`> Gpp Line*1.2: 1.2413793103448276`

`> Gpp Line*1.3: 0.034482758620689655`

Overall, we were just under 50% of lineups cashing (the breakeven point), with tournaments perhaps being a bit more promising (would require a bit more evidence).  While that may not be enough to make money, it does seem to be be better than the average DraftKings player, so at least that is some success.

**What we learned**

We learned how good our lineups really were (or at least got a better idea).  We also learned a lot about scraping websites to generate usable datasets using `requests` and `re` libraries.  Finally, we learned how to use `multiprocessing` to speed up lineup generation.

**What didn't work:**

As mentioned above, we were not able to completely automate the process, and had to collect some of the data manually which became tedious.  Also, it would be interesting to get a more granular sense of how our model performed on a day to day basis, giving us a sense of the variance of which we are working with.