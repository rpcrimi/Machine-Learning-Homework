import math
import numpy as np

#from nflEvaluation import *
def iFunction(y1, y2):
    i = 0.0
    if abs(y1-y2) < 0.0001:
        i = 1.0
    return i
def gFunction(z):
    g = 0
    if z>=8:
        g = 1
    return g
def sFunction(z):
    return 1
#from nflEvaluation import *

def restorePlayType(classType):
    PlayType = math.floor(classType / float(10)) + 1
    Result = classType % 10
    return PlayType, Result


class classifier():
    def switchPlayType(self, PlayType):
        pType = 0
        if abs(PlayType-1) < 0.0001:
            pType = 2
        if abs(PlayType-2) < 0.0001:
            pType = 1
        return pType
    def predict(self,data):
        return np.zeros(len(data))
    def recommendationSingle(self,classType):
        PlayType, Result = restorePlayType(classType)
        if gFunction(Result) < 0.0001:
            PlayType = self.switchPlayType(PlayType)
        return PlayType
    def recommendation(self, predict):
        recommendation = np.zeros(np.size(predict))
        for i in range(np.size(predict)):
            recommendation[i] = self.recommendationSingle(predict[i])
            #print predict[i]
            #print recommendation[i]
        return recommendation
