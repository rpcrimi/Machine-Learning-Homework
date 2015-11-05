from csv import DictReader, DictWriter

import numpy as np
import argparse
import pprint

def extract_data(matches, andor):
    d = []
    if andor == "AND":
        for play in data:
            m = True
            for key, val in matches.iteritems():
                if play[key] != val:
                    m = False

            if m != False:
                d.append(play)

    elif andor == "OR":
        for play in data:
            match = False
            for key, val in matches.iteritems():
                if play[key] == val:
                    match = True

            if match == True:
                d.append(play)
    return d


data = list(DictReader(open("pbp-2014.csv", 'r')))

gameIDs = []
for play in data:
	if play["GameId"] not in gameIDs:
		gameIDs.append(play["GameId"])

for gameID in gameIDs:
	plays = extract_data({"GameId": gameID}, "AND")

	hAverageRush = 0.0
	hAveragePass = 0.0
	hRushAttempts = 0.0
	hPassAttempts = 0.0
	hRushYards = 0.0
	hPassYards = 0.0

	vAverageRush = 0.0
	vAveragePass = 0.0
	vRushAttempts = 0.0
	vPassAttempts = 0.0
	vRushYards = 0.0
	vPassYards = 0.0

	for play in plays:
		if play["IsPass"] == '1' and play["IsIncomplete"] != '1':
			if play["IsPenalty"] == '1':
				if play["PenaltyTeam"] != play["OffenseTeam"]:
					if play["OffenseTeam"] == play["HomeTeam"]:
						hPassAttempts += 1.0
						hPassYards += float(play["Yards"])
						hAveragePass = hPassYards/hPassAttempts
					elif play["OffenseTeam"] == play["VisitingTeam"]:
						vPassAttempts += 1.0
						vPassYards += float(play["Yards"])
						vAveragePass = vPassYards/vPassAttempts
			elif play["IsInterception"] != '1':
				if play["OffenseTeam"] == play["HomeTeam"]:
					hPassAttempts += 1.0
					hPassYards += float(play["Yards"])
					hAveragePass = hPassYards/hPassAttempts
				elif play["OffenseTeam"] == play["VisitingTeam"]:
					vPassAttempts += 1.0
					vPassYards += float(play["Yards"])
					vAveragePass = vPassYards/vPassAttempts

		elif play["IsRush"] == '1':
			if play["IsPenalty"] == '1':
				if play["PenaltyTeam"] != play["OffenseTeam"]:
					if play["OffenseTeam"] == play["HomeTeam"]:
						hRushAttempts += 1.0
						hRushYards += float(play["Yards"])
						hAverageRush = hRushYards/hRushAttempts
					elif play["OffenseTeam"] == play["VisitingTeam"]:
						vRushAttempts += 1.0
						vRushYards += float(play["Yards"])
						vAverageRush = vRushYards/vRushAttempts
			else:
				if play["OffenseTeam"] == play["HomeTeam"]:
					hRushAttempts += 1.0
					hRushYards += float(play["Yards"])
					hAverageRush = hRushYards/hRushAttempts
				elif play["OffenseTeam"] == play["VisitingTeam"]:
					vRushAttempts += 1.0
					vRushYards += float(play["Yards"])
					vAverageRush = vRushYards/vRushAttempts

	print "%s Rush/Pass: %f/%f \t%s Rush/Pass: %f/%f" % (play["HomeTeam"], hAverageRush, hAveragePass, play["VisitingTeam"], vAverageRush, vAveragePass)
