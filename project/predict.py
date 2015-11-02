from csv import DictReader, DictWriter

import numpy as np
import argparse
import pprint

data = list(DictReader(open("pbp-2014.csv", 'r')))
resultsData = list(DictReader(open("results2014.csv", 'r')))

downs = [(str(d), str(t)) for d in range(1, 5) for t in range(1, 11)]

teams = {'BUF': 'Bills',      'BAL': 'Ravens',   'ATL': 'Falcons',  'SEA': 'Seahawks', 
         'GB':  'Packers',    'NO':  'Saints',   'CIN': 'Bengals',  'CHI': 'Bears', 
         'WAS': 'Redskins',   'HOU': 'Texans',   'KC':  'Chiefs',   'TEN': 'Titans',   
         'MIA': 'Dolphins',   'NE':  'Patriots', 'OAK': 'Raiders',  'NYJ': 'Jets', 
         'PHI': 'Eagles',     'JAC': 'Jaguars',  'CLE': 'Browns',   'PIT': 'Steelers', 
         'STL': 'Rams',       'MIN': 'Vikings',  'SF':  '49ers',    'DAL': 'Cowboys', 
         'TB':  'Buccaneers', 'CAR': 'Panthers', 'DEN': 'Broncos',  'IND': 'Colts',    
         'NYG': 'Giants',     'DET': 'Lions',    'SD':  'Chargers', 'ARI': 'Cardinals'}


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

def calculate_score(plays, team1, team2):
    t1Score = 0
    t2Score = 0
    for play in plays:
        touchDownFlag = 0
        puntTDFlag = 0
        if play["IsTouchdown"] == '1':
            splitDescription = play["Description"].split(". ")             
            for i in range(len(splitDescription)):
                if "TOUCHDOWN" in splitDescription[i]:
                    touchDownFlag = 1
                    if "PUNT" not in splitDescription[i]:
                        if play["OffenseTeam"] == team1:
                            t1Score += 6
                        else:
                            t2Score += 6
                    else:
                        puntTDFlag = 1
                        if play["OffenseTeam"] == team1:
                            t2Score += 6
                        else:
                            t1Score += 6

                elif "WAS REVERSED" in splitDescription[i]:
                    if touchDownFlag:
                        if not puntTDFlag:
                            if play["OffenseTeam"] == team1:
                                t1Score -= 6
                            else:
                                t2Score -= 6
                        else:
                            if play["OffenseTeam"] == team1:
                                t2Score -= 6
                            else:
                                t1Score -= 6                                

        elif play["PlayType"] == "EXTRA POINT" and "IS GOOD" in play["Description"]:            
            if play["OffenseTeam"] == team1:
                t1Score += 1
            else:
                t2Score += 1
        elif play["PlayType"] == "FIELD GOAL" and "IS GOOD" in play["Description"]:
            if play["OffenseTeam"] == team1:
                t1Score += 3
            else:
                t2Score += 3
        elif play["IsTwoPointConversionSuccessful"] == "1":
            if play["OffenseTeam"] == team1:
                t1Score += 2
            else:
                t2Score += 2

    return (t1Score, t2Score)


def main():
    games = []
    for team in teams.keys():
        for play in data:
            if play["OffenseTeam"] == team and (play["GameId"], play["OffenseTeam"], play["DefenseTeam"], play["GameDate"]) not in games:
                games.append((play["GameId"], play["OffenseTeam"], play["DefenseTeam"], play["GameDate"]))

    for game in games:
        plays = extract_data({"GameId": game[0]}, "AND")
    
        score = calculate_score(plays, game[1], game[2])

        for result in resultsData:
            if result["kickoff"].split("T")[0] == game[3]:
                if result["home_team"] == game[1]:
                    actualScore = (int(result["home_score"]), int(result["visitors_score"]))
                else:
                    actualScore = (int(result["visitors_score"]), int(result["home_score"]))

        if actualScore != score:
            print "%s vs %s predicted score: %s actual score: %s" % (game[1], game[2], str(score), str(actualScore))

if __name__ == "__main__":
	main()