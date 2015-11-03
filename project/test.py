from csv import DictReader, DictWriter

import numpy as np
import argparse
import pprint

data = list(DictReader(open("pbp-2014.csv", 'r')))

for play in data:
	if "SAFETY" in play["Description"]:
		pprint.pprint(play)