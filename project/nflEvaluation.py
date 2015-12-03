import math
import numpy as np

def restorePlayType(classType):
    PlayType = math.floor(float(classType) / float(10)) + 1
    Result = float(classType) % 10
    return PlayType, Result

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
def s1Function(z):
    return 1
def sFunction(z):
    s = 0
    #10, 1
    if abs(z-10) < 0.0001 or abs(z-1) < 0.0001:
        s = 4
    #9, 2
    elif abs(z-9) < 0.0001 or abs(z-2) < 0.0001:
        s = 3
    #6,7,8,
    elif abs(z-6) < 0.0001 or abs(z-7) < 0.0001 or abs(z-8) < 0.0001:
        s = 2
    #3,4,5
    elif abs(z-3) < 0.0001 or abs(z-4) < 0.0001 or abs(z-5) < 0.0001:
            s = 1
    return s

#weights = {'1': 4, '2': 3, '3': 1, '4': 1, '5': 1, '6': 2, '7': 2, '8': 2, '9': 3, '10': 4, '11': 4, '12': 3, '13': 1, '14': 1, '15': 1, '16': 2, '17': 2, '18': 2, '19': 3, '20': 4}

class evaluation():
    def singleScore(self, actualPlayType, actualResult, recommendPlayType):
        return (-1)**(iFunction(actualPlayType,recommendPlayType)+gFunction(actualResult)) * sFunction(actualResult)
    def Score(actualPlayType, actualResult, recommendPlayType):
        score = 0
        for i in range(len(actualPlayType)):
            score += self.singleScore(actualPlayType[i], actualResult[i], recommendPlayType[i])
        return score
    def singleNum(self, actualPlayType, actualResult, recommendPlayType):
        return (-1)**(iFunction(actualPlayType,recommendPlayType)+gFunction(actualResult)) * s1Function(actualResult)
    def Num(actualPlayType, actualResult, recommendPlayType):
        num = 0
        for i in range(len(actualPlayType)):
            num += self.singleNum(actualPlayType[i], actualResult[i], recommendPlayType[i])
        return num
class classifierEvaluation(evaluation):
    def Score(self, actualClass, RecommendClass):
        score = 0
        num = 0
        typeScore = np.zeros(4)
        typeNum = np.zeros(4)
        for i in range(len(actualClass)):
            actualPlayType, actualResult = restorePlayType(actualClass[i])
            recommendPlayType, recommendResult = restorePlayType(RecommendClass[i])

            score += self.singleScore(actualPlayType, actualResult, recommendPlayType)

            num += self.singleNum(actualPlayType, actualResult, recommendPlayType)
            typeNum[classifyResultType(actualPlayType, actualResult, recommendPlayType) - 1] += 1

        return score, num, typeNum
