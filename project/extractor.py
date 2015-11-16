from csv import DictReader, DictWriter
import numpy as np

def classifyPlayType(PlayType, typelist):
    for i in range(len(typelist)):
        value = len(typelist)
        if PlayType == typelist[i]:
            value = i
            break
    return value

class Extractor():
    def extract(self, data):
        return data

class PbpExtractor(Extractor):
    def buildPlayTypeList(self, data):
        self.typelist = []
        for play in data:
            if play["PlayType"] not in self.typelist:
                self.typelist.append(play["PlayType"])
    def extract(self, data):
        self.buildPlayTypeList(data)
        featureNum = 6
        target = np.zeros(len(data))
        feature= np.zeros((len(data), featureNum))
        i = 0
        for play in data:
            typeCheck = classifyPlayType(play["PlayType"], self.typelist)
            if typeCheck != 0:
                Time  = 15* 60 - (int(play["Minute"]) * 60  + int(play["Second"]) )
                feature[i,:] = np.matrix([int(play["Quarter"]), Time, int(play["Down"]), int(play["ToGo"]), int(play["YardLine"]), int(play["SeriesFirstDown"]) ])
                target[i] = typeCheck
                i += 1
            featureFinal = feature[0:(i-1),:]
            targetFinal = target[0:(i-1)]
        return featureFinal, targetFinal

def resultMapping(PlayResult):
    return {
        '1': -4,
        '2': -2,
        '3': -2,
        '4': -2,
        '5': -1,
        '6': -1,
        '7': -1,
        '8': 2,
        '9': 3,
        '10': 4,
    }.get(PlayResult, 0)

class NewPbpExtractor(Extractor):
    def seperateY(self, datalist):
        PlayType = datalist["Y"][1]
        PlayResult = datalist["Y"][4]
        return PlayType, PlayResult
    def extract(self, data):
        featureNum = 6
        pType = np.zeros(len(data))
        pScore = np.zeros(len(data))
        feature= np.zeros((len(data), featureNum))

        i = 0
        for play in data:
            PlayType, PlayResult = self.seperateY(play)
            if PlayType in self.typeList:
                Time  = 15* 60 - (int(play["Minute"]) * 60  + int(play["Second"]) )
                feature[i,:] = np.matrix([int(play["Quarter"]), Time, int(play["Down"]), int(play["ToGo"]), int(play["YardLine"]), int(play["SeriesFirstDown"]) ])

                PlayScore = resultMapping(PlayResult)

                pType[i] = PlayType
                pScore[i] = PlayScore
                i += 1

        featureFinal = feature[0:(i-1),:]
        pFinal = pType[0:(i-1)]
        sFinal = pScore[0:(i-1)]
        return featureFinal, pFinal, sFinal


data = list(DictReader(open("pbp-2014.csv", 'r')))
pbp2014 = NewPbpExtractor()
typeList = [0,1,2]
pbp2014.typeList = typeList
pbp2014.extract(data)
#pbp2014 = PbpExtractor()
#pbp2014.buildPlayTypeList(data)
#print len(data)
#print classifyPlayType(data[0]["PlayType"], pbp2014.typelist) != 0
