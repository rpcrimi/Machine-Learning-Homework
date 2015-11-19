
from csv import DictReader, DictWriter

from extractor import NewPbpExtractor
from nflClassifier import *
from nflEvaluation import *

class BayesClassifier(classifier):
    def __init__(self):
        from sklearn.naive_bayes import GaussianNB
        self.gnb = GaussianNB()
    def classify(self, data, target):
        self.gnb.fit(data, target)
        y_pred = self.gnb.predict(data)
        return y_pred
    def predict(self, data):
        return self.gnb.predict(data)

data = list(DictReader(open("pbp-2014.csv", 'r')))
pbp2014 = NewPbpExtractor()
feature, target = pbp2014.extract4Classifier(data)
#print target

byClassifer = BayesClassifier()
byClassifer.classify(feature, target)
temp = byClassifer.predict(feature)
y_pred = byClassifer.recommendation(byClassifer.predict(feature))
#print y_pred
print("Number of a total %d points" % len(target) )
class2014 = classifierEvaluation()
print class2014.Score(target, temp)
print class2014.Score(target, y_pred)
