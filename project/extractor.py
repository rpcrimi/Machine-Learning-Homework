from csv import DictReader, DictWriter
import numpy as np
import re
from nflEvaluation import sFunction

def classifyType(Type, typelist):
    for i in range(len(typelist)):
        value = len(typelist)
        if Type == typelist[i]:
            value = i
            break
    return value

def seperateVector(datalist):
    temp = str(datalist)
    temp1 = re.findall(r'\b\d+\b', temp)
    return temp1[0], temp1[1]

def numericalYardLineDirection(data):
    if data == "OWN":
        z = 1
    elif data == "OPP":
        z = 2
    else:
        z = 3
    return z

def isHomeTeambeOffenseTeam(HomeTeam, OffenseTeam, CurrentScore):
    HomeScore, VisitScore = seperateVector(CurrentScore)
    z = 0
    if  HomeTeam == OffenseTeam:
        z = 1
        OffenseScore = HomeScore
        DefScore = VisitScore
    else:
        OffenseScore = VisitScore
        DefScore = HomeScore
    return z, OffenseScore, DefScore

def yards(data):
     try:
         z = int(data)
         #break
     except ValueError:
         z = 0
     return z

class Extractor():
    def buildPlayTypeList(self, data):
        self.typelist = []
        for play in data:
            if play["PlayType"] not in self.typelist:
                self.typelist.append(play["PlayType"])
    def buildFormationList(self, data):
        self.formationlist = []
        for play in data:
            if play["Formation"] not in self.formationlist:
                self.formationlist.append(play["Formation"])
    #def extract(self, data):
    #    return data

class PbpExtractor(Extractor):
    def extract(self, data):
        self.buildPlayTypeList(data)
        featureNum = 6
        target = np.zeros(len(data))
        feature= np.zeros((len(data), featureNum))
        i = 0
        for play in data:
            typeCheck = classifyType(play["PlayType"], self.typelist)
            if typeCheck != 0:
                Time  = 15* 60 - (int(play["Minute"]) * 60  + int(play["Second"]) )
                feature[i,:] = np.matrix([int(play["Quarter"]), Time, int(play["Down"]), int(play["ToGo"]), int(play["YardLine"]), int(play["SeriesFirstDown"]) ])
                target[i] = typeCheck
                i += 1
            featureFinal = feature[0:(i-1),:]
            targetFinal = target[0:(i-1)]
        return featureFinal, targetFinal

class NewPbpExtractor(Extractor):
    def extract(self, data):
        featureNum = 12
        pType = np.zeros(len(data))
        pScore = np.zeros(len(data))
        pResult = np.zeros(len(data))
        feature= np.zeros((len(data), featureNum))

        i = 0
        for play in data:
            PlayType, PlayResult = seperateVector(play["Y"])
            Formation = classifyType(play["Formation"], self.formationlist)
            Time  = 15* 60 - (int(play["Minute"]) * 60  + int(play["Second"]) )
            YardLineDirection = numericalYardLineDirection(play["YardLineDirection"])
            HomeTeambeOffenseTeam, OffenseScore, DefScore = isHomeTeambeOffenseTeam(play["HomeTeam"], play["OffenseTeam"], play["CurrentScore"])
            Yards = yards(play["Yards"])
            feature[i,:] = np.matrix([int(play["Quarter"]), Time, int(play["Down"]), int(play["ToGo"]), int(play["YardLine"]), int(play["SeriesFirstDown"]), Yards, YardLineDirection, HomeTeambeOffenseTeam, Formation, OffenseScore, DefScore ])

            pType[i] = PlayType
            pResult[i] = PlayResult
            i += 1

        featureFinal = feature[0:(i-1),:]
        pFinal = pType[0:(i-1)]
        rFinal = pResult[0:(i-1)]
        return featureFinal, pFinal, rFinal

    def extract4Classifier(self, data):
        feature, pFinal, rFinal = self.extract(data)
        featureClass= np.zeros((np.size(feature,0), np.size(feature,1)))
        itemClass = np.zeros(len(pFinal))
        i = 0
        for j in range(len(feature)):
            if abs(pFinal[j] - 0 ) > .0001 and abs(rFinal[j] - 0 ) > .0001 and abs(feature[j,2]-0) > .0001 and abs(feature[j,2]-4) > .0001:
                featureClass[i,:] = feature[j,:]
                itemClass[i] = int(rFinal[j] + (pFinal[j] - 1)*10)
                i += 1

        return featureClass[0:(i-1),:], itemClass[0:(i-1)]
