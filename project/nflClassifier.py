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

class knClassifier(classifier):#done
    def __init__(self, n_neighbors=5, algorithm="auto", metric="minkowski"):
        self.name = "KNeighborsClassifier, n_neighbors %d, algorithm=%s, metric=%s" % (n_neighbors, algorithm, metric )
        from sklearn.neighbors import KNeighborsClassifier
        self.clf = KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=algorithm, metric=metric)
class svmClassifier(classifier):
    def __init__(self, C=1.0, kernel="rbf"):
        from sklearn.svm  import SVC
        self.name = "svmClassifier, C=%d, kernel: %s)" %(C, kernel)
        self.clf = SVC(C=C, kernel=kernel)
class BayesClassifier(classifier):#done
    def __init__(self):
        self.name = "GaussianNB"
        from sklearn.naive_bayes import GaussianNB
        self.clf = GaussianNB()
class BernoulliNB(classifier):#done
    def __init__(self):
        self.name = "BernoulliNB"
        from sklearn.naive_bayes import BernoulliNB
        self.clf = BernoulliNB()
'''
class MultinomialNB(classifier):
    def __init__(self):
        self.name = "MultinomialNB"
        from sklearn.naive_bayes import MultinomialNB
        self.clf = MultinomialNB()
'''
class dtClassifier(classifier):#done
    def __init__(self, max_depth=5, splitter="best", random_state=0, max_features=None):
        self.name = "DecisionTreeClassifier, max_depth %s, splitter %s, max_features %s" % (str(max_depth), splitter, str(max_features))
        from sklearn.tree import DecisionTreeClassifier
        self.clf = DecisionTreeClassifier(max_depth=max_depth, splitter=splitter, max_features=max_features)
class rfClassifier(classifier):#done
    def __init__(self, max_depth=None, criterion="gini", max_features="auto"):
        self.name = "RandomForestClassifier, max_depth %s, criterion %s, max_features %s" % (str(max_depth), criterion, str(max_features))
        from sklearn.ensemble import RandomForestClassifier
        self.clf = RandomForestClassifier(max_depth=max_depth, criterion=criterion, max_features=max_features)
class adaBoostClassifier(classifier):#done
    def __init__(self, method="dt", algorithm="SAMME.R"):
        from sklearn.ensemble import AdaBoostClassifier
        self.name = "AdaBoostClassifier, method-%s, algorithm-%s" % (method, algorithm)
        if method == "dt":
            self.clf = AdaBoostClassifier(algorithm=algorithm)
        if method =="svm":
            from sklearn.svm import SVC
            self.clf = AdaBoostClassifier(SVC(probability=True,kernel='linear'), algorithm=algorithm, n_estimators=10)
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
