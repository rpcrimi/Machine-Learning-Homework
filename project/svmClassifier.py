#import math
from csv import DictReader, DictWriter

from extractor import NewPbpExtractor
from nflClassifier import *
from nflEvaluation import *

class svmClassifier(classifier):
    def __init__(self):
        from sklearn import svm
        self.clf = svm.SVC(gamma=0.001, C=100.)
    def classify(self, data, target):
        self.clf.fit(data, target)
    def predict(self, data):
        return self.clf.predict(data)

data = list(DictReader(open("pbp-2014&13.csv", 'r')))
pbp2014 = NewPbpExtractor()
feature, target = pbp2014.extract4Classifier(data)
svmClassifer = svmClassifier()
svmClassifer.classify(feature, target)
temp = svmClassifer.predict(feature)
y_pred = svmClassifer.recommendation(temp)
#print y_pred
print("Number of mislabeled points out of a total %d points : %d" % (len(target),(target != y_pred).sum()))
class2014 = classifierEvaluation()
#print class2014.Score(target, temp)
print class2014.Score(target, y_pred)
