from csv import DictReader, DictWriter

import numpy as np
import argparse
import pprint

months = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05",
"June": "06", "July": "07", "Auguest": "08", "September": "09", "October": "10",
"November": "11", "December": "12"}

teams = {}

data = list(DictReader(open("pbp-2015.csv", 'r')))
results = list(DictReader(open("results2015.csv", 'r')))


with open("pbp-2015New.csv", "w") as csvFile:
	fieldnames = ["GameId","GameDate","Quarter","Minute","Second","OffenseTeam","DefenseTeam","Down","ToGo","YardLine","SeriesFirstDown","Description","SeasonYear","Yards","Formation","PlayType","IsRush","IsPass","IsIncomplete","IsTouchdown","PassType","IsSack","IsChallenge","IsChallengeReversed","IsInterception","IsFumble","IsPenalty","IsTwoPointConversion","IsTwoPointConversionSuccessful","RushDirection","YardLineFixed","YardLineDirection","IsPenaltyAccepted","PenaltyTeam","IsNoPlay","PenaltyType","PenaltyYards","HomeTeam","VisitingTeam","HomeTeamFinalScore","VisitingTeamFinalScore", "Y", "CurrentScore"]
	writer = DictWriter(csvFile, fieldnames=fieldnames, extrasaction='ignore')
	writer.writeheader()

	for result in results:
		if "Week" not in result["Week"]:
			month = months[result["Date"].split()[0]]
			day = result["Date"].split()[1]
			date = "2015%s%02d" % (month, int(day))
			
			if "@" in result.values():
				HomeTeam = result["Loser/tie"]
				HomeTeamScore = result["PtsL"]
				VisitingTeam = result["Winner/tie"]
				VisitingTeamScore = result["PtsW"]
			else:
				HomeTeam = result["Winner/tie"]
				HomeTeamScore = result["PtsW"]
				VisitingTeam = result["Loser/tie"]	
				VisitingTeamScore = result["PtsL"]

			if HomeTeam not in teams:
				HT = raw_input("%s: " % (HomeTeam))
				teams[HomeTeam] = HT
			
			if VisitingTeam not in teams:
				VT = raw_input("%s: " % (VisitingTeam))
				teams[VisitingTeam] = VT

			for play in data:
				if play["GameId"][:-2] == date and (play["DefenseTeam"] == teams[HomeTeam] or play["DefenseTeam"] == teams[VisitingTeam]):
					play["HomeTeam"] = teams[HomeTeam]
					play["HomeTeamFinalScore"] = HomeTeamScore
					play["VisitingTeam"] = teams[VisitingTeam]
					play["VisitingTeamFinalScore"] = VisitingTeamScore
					writer.writerow(play)
