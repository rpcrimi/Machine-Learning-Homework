from csv import DictReader, DictWriter

import numpy as np
import argparse
import pprint

data = list(DictReader(open("pbp-2014.csv", 'r')))

for play in data:
	if play["OffenseTeam"] == "BUF" and play["DefenseTeam"] == "MIA" and play["HomeTeamFinalScore"] == '29':
		pprint.pprint(play)
		break