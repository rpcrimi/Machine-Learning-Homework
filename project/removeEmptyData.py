from csv import DictReader, DictWriter

import numpy as np
import argparse
import pprint

data = list(DictReader(open("pbp-2014.csv", 'r')))

with open("pbp-2014New.csv", "w") as csvFile:
    fieldnames = ["GameId","GameDate","Quarter","Minute","Second","OffenseTeam","DefenseTeam","Down","ToGo","YardLine","SeriesFirstDown","Description","SeasonYear","Yards","Formation","PlayType","IsRush","IsPass","IsIncomplete","IsTouchdown","PassType","IsSack","IsChallenge","IsChallengeReversed","IsInterception","IsFumble","IsPenalty","IsTwoPointConversion","IsTwoPointConversionSuccessful","RushDirection","YardLineFixed","YardLineDirection","IsPenaltyAccepted","PenaltyTeam","IsNoPlay","PenaltyType","PenaltyYards","HomeTeam","VisitingTeam","HomeTeamFinalScore","VisitingTeamFinalScore"]
    writer = DictWriter(csvFile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()

    for play in data:
        del play["NextScore"]
        del play["IsMeasurement"]
        del play["Challenger"]
        del play["TeamWin"]

        writer.writerow(play)
