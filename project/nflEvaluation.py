import math
import numpy as np

#from nflClassifier import restorePlayType
def restorePlayType(classType):
    PlayType = math.floor(classType / float(10)) + 1
    Result = classType % 10
    return PlayType, Result
#from nflClassifier import restorePlayType

def classifyResultType(actualPlayType,actualResult, recommendPlayType):
    if gFunction(actualResult) == 1:
        if abs(recommendPlayType - actualPlayType) < 0.0001:
            ResultType = 1
        else:
            ResultType = 3
    else:
        if abs(recommendPlayType - actualPlayType) < 0.0001:
            ResultType = 4
        else:
            ResultType = 2
    return ResultType

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


class evaluation():
    def singleScore(self, actualPlayType, actualResult, recommendPlayType):
        #print actualPlayType
        #print recommendPlayType
        #print self.iFunction(actualPlayType,recommendPlayType)
        #print self.gFunction(actualResult)
        return (-1)**(iFunction(actualPlayType,recommendPlayType)+gFunction(actualResult)) * sFunction(actualResult)
    def Score(actualPlayType, actualResult, recommendPlayType):
        score = 0
        for i in range(len(actualPlayType)):
            score += self.singleScore(actualPlayType[i], actualResult[i], recommendPlayType[i])
        return score

class classifierEvaluation(evaluation):
    def Score(self, actualClass, RecommendClass):
        score = 0
        typeScore = np.zeros(4)
        for i in range(len(actualClass)):
            actualPlayType, actualResult = restorePlayType(actualClass[i])
            recommendPlayType, recommendResult = restorePlayType(RecommendClass[i])

            score += self.singleScore(actualPlayType, actualResult, recommendPlayType)
            typeScore[classifyResultType(actualPlayType, actualResult, recommendPlayType) - 1] += 1

        return score, typeScore
