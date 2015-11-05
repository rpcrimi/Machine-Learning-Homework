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

def calculate_score(plays, homeTeam, visitingTeam):
    homeScore = 0
    visitingScore = 0
    for play in plays:
        offTDFlag = 0
        defTDFlag = 0
        extraPointFlag = 0
        twoPointConversionFlag = 0
        fieldGoalFlag = 0
        safetyFlag = 0
        if play["IsTouchdown"] == '1':

            if "INTERCEPTED" in play["Description"] or "PUNT" in play["Description"] or "FUMBLE" in play["Description"] or "KICKS" in play["Description"]:
                addScore = 7
                splitDescription = play["Description"].split(". ")
                for desc in splitDescription:
                    if "INTERCEPTED" in desc or "PUNT" in desc or "FUMBLE" in desc or "KICKS" in desc:
                        if "KICKS" in desc:
                            addScore = 6
                        defTDFlag = 1
                        if play["DefenseTeam"] == homeTeam:
                            homeScore += addScore
                        elif play["DefenseTeam"] == visitingTeam:
                            visitingScore += addScore
                    elif "WAS REVERSED" in desc and defTDFlag:
                        if play["DefenseTeam"] == homeTeam:
                            homeScore -= addScore
                        elif play["DefenseTeam"] == visitingTeam:
                            visitingScore -= addScore
                        defTDFlag = 0

                if int(play["IsPenalty"]) and defTDFlag:
                    if play["PenaltyTeam"] == play["DefenseTeam"] and play["IsPenaltyAccepted"] == '1' and "ENFORCED BETWEEN DOWNS" not in play["Description"]:
                        if play["DefenseTeam"] == homeTeam:
                            homeScore -= addScore
                        elif play["DefenseTeam"] == visitingTeam:
                            visitingScore -= addScore

            else:
                addScore = 6
                splitDescription = play["Description"].split(". ")             
                for desc in splitDescription:
                    if "TOUCHDOWN" in desc:
                        offTDFlag = 1

                        if play["OffenseTeam"] == homeTeam:
                            homeScore += addScore
                        elif play["OffenseTeam"] == visitingTeam:
                            visitingScore += addScore

                    elif "WAS REVERSED" in desc:
                        if offTDFlag:
                            if play["OffenseTeam"] == homeTeam:
                                homeScore -= addScore
                            elif play["OffenseTeam"] == visitingTeam:
                                visitingScore -= addScore
                            offTDFlag = 0

                if int(play["IsPenalty"]) and offTDFlag:
                    if play["PenaltyTeam"] == play["OffenseTeam"] and play["IsPenaltyAccepted"] == '1' and "ENFORCED BETWEEN DOWNS" not in play["Description"]:
                        if play["OffenseTeam"] == homeTeam:
                            homeScore -= addScore
                        elif play["OffenseTeam"] == visitingTeam:
                            visitingScore -= addScore
                        offTDFlag = 0  

        elif play["PlayType"] == "EXTRA POINT" and "IS GOOD" in play["Description"] and play["IsNoPlay"] != '1':
            if play["OffenseTeam"] == homeTeam:
                homeScore += 1
            elif play["OffenseTeam"] == visitingTeam:
                visitingScore += 1
            if play["IsPenaltyAccepted"] == '1' and play["OffenseTeam"] == play["PenaltyTeam"] and "ENFORCED BETWEEN DOWNS" not in play["Description"]:
                if play["OffenseTeam"] == homeTeam:
                    homeScore -= 1
                elif play["OffenseTeam"] == visitingTeam:
                    visitingScore -= 1  

        elif play["PlayType"] == "FIELD GOAL" and "IS GOOD" in play["Description"] and play["IsNoPlay"] != '1':
            if play["OffenseTeam"] == homeTeam:
                homeScore += 3
            elif play["OffenseTeam"] == visitingTeam:
                visitingScore += 3
            if play["IsPenaltyAccepted"] == '1' and play["OffenseTeam"] == play["PenaltyTeam"] and "ENFORCED BETWEEN DOWNS" not in play["Description"]:
                if play["OffenseTeam"] == homeTeam:
                    homeScore -= 3
                elif play["OffenseTeam"] == visitingTeam:
                    visitingScore -= 3 

        elif play["IsTwoPointConversion"] == "1":
            splitDescription = play["Description"].split(". ")
            for desc in splitDescription:
                if "ATTEMPT SUCCEEDS" in desc:
                    twoPointConversionFlag = 1
                    if play["OffenseTeam"] == homeTeam:
                        homeScore += 2
                    elif play["OffenseTeam"] == visitingTeam:
                        visitingScore += 2
                elif "WAS REVERSED" in desc and twoPointConversionFlag:
                    if play["OffenseTeam"] == homeTeam:
                        homeScore += 2
                    elif play["OffenseTeam"] == visitingTeam:
                        visitingScore += 2
                    twoPointConversionFlag = 0                    

            if play["IsPenaltyAccepted"] == '1' and play["OffenseTeam"] == play["PenaltyTeam"] and "ENFORCED BETWEEN DOWNS" not in play["Description"]:
                if play["OffenseTeam"] == homeTeam:
                    homeScore -= 2
                elif play["OffenseTeam"] == visitingTeam:
                    visitingScore -= 2

        elif "SAFETY" in play["Description"]:
            splitDescription = play["Description"].split(". ")
            for desc in splitDescription:
                if "SAFETY" in desc:
                    safetyFlag = 1
                    if play["DefenseTeam"] == homeTeam:
                        homeScore += 2
                    elif play["DefenseTeam"] == visitingTeam:
                        visitingScore += 2                   

                elif "WAS REVERSED" in desc and safetyFlag:
                    if play["DefenseTeam"] == homeTeam:
                        homeScore -= 2
                    elif play["DefenseTeam"] == visitingTeam:
                        visitingScore -= 2
                    safetyFlag = 0

            if play["IsPenaltyAccepted"] == '1' and play["PenaltyTeam"] == play["DefenseTeam"] and safetyFlag and "ENFORCED BETWEEN DOWNS" not in play["Description"]:
                if play["DefenseTeam"] == homeTeam:
                    homeScore -= 2
                elif play["DefenseTeam"] == visitingTeam:
                    visitingScore -= 2         

    return (homeScore, visitingScore)


def main():
    games = []
    numGames = 0
    numGamesWrong = 0

    for play in data:
        idExists = 0
        for game in games:
            if play["GameId"] in game[0]:
                idExists = 1
                break
        if idExists == 0:
            games.append([play["GameId"], play["HomeTeam"], play["VisitingTeam"]])

    for game in games:
        plays = extract_data({"GameId": game[0]}, "AND")
        score = calculate_score(plays, game[1], game[2])

        for play in data:
            if play["GameId"] == game[0]:
                actualScore = (int(play["HomeTeamFinalScore"]), int(play["VisitingTeamFinalScore"]))
                break

        numGames += 1
        if actualScore != score:
            numGamesWrong += 1
            print "%s vs %s \tpredicted score: %s \tactual score: %s" % (game[1], game[2], str(score), str(actualScore))

    print "Num Game: %d Num Wrong: %d" % (numGames, numGamesWrong)

if __name__ == "__main__":
	main()