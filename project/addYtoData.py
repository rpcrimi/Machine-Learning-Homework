from csv import DictReader, DictWriter
import numpy as np
import argparse
import pprint

TOUCHDOWN = 10
FIRST_DOWN = 9
SIGNIFICANT_YARDS = 8
NOT_ENOUGH_YARDS = 7
LOSS_OF_YARDS = 6
FOURTH_DOWN = 5
FUMBLE = 4
INTERCEPTION = 3
SAFETY = 2
DEF_TOUCHDOWN = 1
NOT_PASS_RUSH = 0

data = list(DictReader(open("pbp-2013.csv", 'r')))

with open("pbp-2013New.csv", "w") as csvFile:
	fieldnames = ["GameId","GameDate","Quarter","Minute","Second","OffenseTeam","DefenseTeam","Down","ToGo","YardLine","SeriesFirstDown","Description","SeasonYear","Yards","Formation","PlayType","IsRush","IsPass","IsIncomplete","IsTouchdown","PassType","IsSack","IsChallenge","IsChallengeReversed","IsInterception","IsFumble","IsPenalty","IsTwoPointConversion","IsTwoPointConversionSuccessful","RushDirection","YardLineFixed","YardLineDirection","IsPenaltyAccepted","PenaltyTeam","IsNoPlay","PenaltyType","PenaltyYards","HomeTeam","VisitingTeam","HomeTeamFinalScore","VisitingTeamFinalScore", "Y"]
	writer = DictWriter(csvFile, fieldnames=fieldnames, extrasaction='ignore')
	writer.writeheader()

	for play in data:
		if play["PlayType"] in ["PASS", "RUSH"]:
			if play["PlayType"] == "PASS":
				Y = [1, NOT_PASS_RUSH]
			else:
				Y = [2, NOT_PASS_RUSH]

			offTDFlag = 0
			defTDFlag = 0
			if play["IsTouchdown"] == '1':
				if "INTERCEPTED" in play["Description"] or "PUNT" in play["Description"] or "FUMBLE" in play["Description"] or "KICKS" in play["Description"]:
					result = DEF_TOUCHDOWN
				else:
					result = TOUCHDOWN
			else:
				if int(play["IsFumble"]):
					result = FUMBLE
				elif int(play["IsInterception"]):
					result = INTERCEPTION
				elif "SAFETY" in play["Description"]:
					result = SAFETY
				else:
					down = float(play["Down"])
					toGo = float(play["ToGo"])
					yards = float(play["Yards"])
					if down != 4.0:
						numTries = 4.0 - down
					else:
						numTries = 1.0

					if yards >= toGo:
						result = FIRST_DOWN
					elif yards < 0:
						result = LOSS_OF_YARDS
					elif toGo/numTries < yards:
						result = SIGNIFICANT_YARDS
					else:
						if int(play["Down"]) == 3:
							result = FOURTH_DOWN
						else:
							result = NOT_ENOUGH_YARDS
			Y[1] = result

		else:
			Y = [0, NOT_PASS_RUSH]

		play["Y"] = Y
		writer.writerow(play)


