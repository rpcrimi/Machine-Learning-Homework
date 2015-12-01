
from csv import DictReader, DictWriter

from extractor import NewPbpExtractor
from nflClassifier import *
from nflEvaluation import *

class knClassifier(classifier):
    def __init__(self):
        from sklearn.neighbors import KNeighborsClassifier
        self.gnb = GaussianNB()
    def classify(self, data, target):
        self.gnb.fit(data, target)
        y_pred = self.gnb.predict(data)
        return y_pred
    def predict(self, data):
        return self.gnb.predict(data)

#training
data = list(DictReader(open("pbp-2014.csv", 'r')))
data2014 = list(DictReader(open("pbp-2013.csv", 'r')))
data.extend(data2014)

pbp2014 = NewPbpExtractor()
pbp2014.buildFormationList(data)
feature, target = pbp2014.extract4Classifier(data)
byClassifer = BayesClassifier()
byClassifer.classify(feature, target)

#test
#data2015 = list(DictReader(open("pbp-2015.csv", 'r')))
data2015 = list(DictReader(open("pbp-2014.csv", 'r')))
feature2015, target2015 = pbp2014.extract4Classifier(data2015)

temp = byClassifer.predict(feature2015)
y_pred = byClassifer.recommendation(temp)

print("Number of a total %d points" % len(target2015) )
class2014 = classifierEvaluation()
print class2014.Score(target2015, y_pred)
