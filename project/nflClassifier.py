import math
import numpy as np

from nflEvaluation import iFunction, gFunction, sFunction, restorePlayType

class classifier():
    def classify(self, data, target, needWeight=False):
        X, Y = data, target
        if needWeight:
            X, Y = self.manualWeight(data, target)
        self.clf.fit(X, Y)
    def predict(self, data):
        return self.clf.predict(data)
    def switchPlayType(self, PlayType):
        pType = 0
        if abs(PlayType-1) < 0.0001:
            pType = 2
        if abs(PlayType-2) < 0.0001:
            pType = 1
        return pType
    def manualWeight(self, data, target):
        w=0
        X = np.zeros((np.size(data,0)*4, np.size(data,1)))
        Y = np.zeros(len(target)*4)
        for i in range(len(data)):
            PlayType, Result = restorePlayType(target[i])
            for j in range(sFunction(Result)):
                X[w,:] = data[i,:]
                Y[w] = target[i]
                w += 1
        return X, Y

    def recommendationSingle(self,classType):
        PlayType, Result = restorePlayType(classType)
        if gFunction(Result) < 0.0001:
            PlayType = self.switchPlayType(PlayType)
        recommendationCalss = (PlayType-1)*10 + Result
        return recommendationCalss
    def recommendation(self, predict):
        recommendation = np.zeros(np.size(predict))
        for i in range(np.size(predict)):
            recommendation[i] = self.recommendationSingle(predict[i])
        return recommendation

class knClassifier(classifier):
    def __init__(self):
        self.name = "KNeighborsClassifier"
        from sklearn.neighbors import KNeighborsClassifier
        self.clf = KNeighborsClassifier(4)
class svmClassifier(classifier):
    def __init__(self):
        self.name = "svmClassifier, gamma=0.001, C=100.)"
        from sklearn import svm
        self.clf = svm.SVC(gamma=0.001, C=100.)
    def linear(self, C=0.025):
        self.name = "svmClassifier, linear, C=%d" % (C)
        from sklearn import svm
        self.clf = svm.SVC(kernel="linear", C=C)
    def gamma(self, gamma=2, C=1):
        self.name = "svmClassifier, gamma, C=%d" % (C)
        from sklearn import svm
        self.clf = svm.SVC(gamma=gamma, C=C)
class BayesClassifier(classifier):
    def __init__(self):
        self.name = "GaussianNB"
        from sklearn.naive_bayes import GaussianNB
        self.clf = GaussianNB()
class dtClassifier(classifier):
    def __init__(self):
        self.name = "DecisionTreeClassifier"
        from sklearn.tree import DecisionTreeClassifier
        self.clf = DecisionTreeClassifier(max_depth=5)
class rfClassifier(classifier):
    def __init__(self):
        self.name = "RandomForestClassifier"
        from sklearn.ensemble import RandomForestClassifier
        self.clf = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
class adaBoostClassifier(classifier):
    def __init__(self):
        self.name = "AdaBoostClassifier"
        from sklearn.ensemble import AdaBoostClassifier
        self.clf = AdaBoostClassifier()
'''
class ldClassifier(classifier):
    def __init__(self):
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
        self.clf =  LinearDiscriminantAnalysis()
class qdClassifier(classifier):
    def __init__(self):
        from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
        self.clf = QuadraticDiscriminantAnalysis()
'''
