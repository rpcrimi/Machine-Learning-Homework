from csv import DictReader, DictWriter

import numpy as np
import argparse
import pprint

data = list(DictReader(open("pbp-2013.csv", 'r')))
resultsData = list(DictReader(open("results2013.csv", 'r')))

for play in data:
	gameID = play["GameId"]
	gameDate = play["GameDate"]

	if play["OffenseTeam"] == '':
		for p in data:
			if p["GameId"] == gameID and p["OffenseTeam"] != '' and p["DefenseTeam"] == play["DefenseTeam"]:
				play["OffenseTeam"] = p["OffenseTeam"]
				break
	for result in resultsData:
		if result["kickoff"].split("T")[0] == gameDate:
			if result["home_team"] in [play["OffenseTeam"], play["DefenseTeam"]]:
				homeTeam = result["home_team"]
				awayTeam = result["visiting_team"]
				r = result
				break

	if homeTeam == play["DefenseTeam"]:
		play["HomeTeam"] = play["DefenseTeam"]
		play["VisitingTeam"] = play["OffenseTeam"]
	else:
		play["HomeTeam"] = play["OffenseTeam"]
		play["VisitingTeam"] = play["DefenseTeam"]

	play["HomeTeamFinalScore"] = r["home_score"]
	play["VisitingTeamFinalScore"] = r["visitors_score"]

with open("pbp-2013New.csv", "w") as csvFile:
	fieldnames = ["GameId","GameDate","Quarter","Minute","Second","OffenseTeam","DefenseTeam","Down","ToGo","YardLine","SeriesFirstDown","NextScore","Description","TeamWin","SeasonYear","Yards","Formation","PlayType","IsRush","IsPass","IsIncomplete","IsTouchdown","PassType","IsSack","IsChallenge","IsChallengeReversed","Challenger","IsMeasurement","IsInterception","IsFumble","IsPenalty","IsTwoPointConversion","IsTwoPointConversionSuccessful","RushDirection","YardLineFixed","YardLineDirection","IsPenaltyAccepted","PenaltyTeam","IsNoPlay","PenaltyType","PenaltyYards","HomeTeam","VisitingTeam","HomeTeamFinalScore","VisitingTeamFinalScore"]
	writer = DictWriter(csvFile, fieldnames=fieldnames, extrasaction='ignore')
	writer.writeheader()

	for play in data:
		writer.writerow(play)
