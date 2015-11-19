import math

class evaluation():
    def iFunction(self, y1, y2):
        i = 0.0
        if abs(y1-y2) < 0.0001:
            check = 1.0
        return i
    def gFunction(self, z):
        g = 0
        if z>=8:
            g = 1
        return g
    def sFunction(self, z):
        return 1
    def singleScore(self, actualPlayType, actualResult, recommendPlayType):
        return (-1)**(self.iFunction(actualPlayType,recommendPlayType)+self.gFunction(actualResult)) * self.sFunction(actualResult)
    def Score(actualPlayType, actualResult, recommendPlayType):
        score = 0
        for i in range(len(actualPlayType)):
            score += self.singleScore(actualPlayType[i], actualResult[i], recommendPlayType[i])
        return score

class classifierEvaluation(evaluation):
    def Score(self, actualClass, RecommendClass):
        score = 0
        for i in range(len(actualClass)):
            actualPlayType = math.floor(actualClass[i] / float(10))
            actualResult = actualClass[i] % 10
            recommendPlayType = math.floor(RecommendClass[i] / float(10))
            score += self.singleScore(actualPlayType, actualResult, recommendPlayType)
        return score
