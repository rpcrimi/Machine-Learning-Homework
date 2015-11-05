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

class PbpExtractor():
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
        #target = []
        i = 0
        for play in data:
            typeCheck = classifyPlayType(play["PlayType"], self.typelist)
            #print typeCheck
            #if True:
            if typeCheck != 0:
                #print typeCheck
                Time  = 15* 60 - (int(play["Minute"]) * 60  + int(play["Second"]) )
                feature[i,:] = np.matrix([int(play["Quarter"]), Time, int(play["Down"]), int(play["ToGo"]), int(play["YardLine"]), int(play["SeriesFirstDown"]) ])
                target[i] = typeCheck
                i += 1
            featureFinal = feature[0:(i-1),:]
            targetFinal = target[0:(i-1)]
        return featureFinal, targetFinal

'''
data = list(DictReader(open("pbp-2014.csv", 'r')))
pbp2014 = PbpExtractor()
pbp2014.buildPlayTypeList(data)
print len(data)
print classifyPlayType(data[0]["PlayType"], pbp2014.typelist) != 0
'''
