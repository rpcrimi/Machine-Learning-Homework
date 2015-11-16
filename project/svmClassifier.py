
from csv import DictReader, DictWriter
from extractor import PbpExtractor
from bayesClassifier import Classifier



class svmClassifier(Classifier):
    def __init__(self):
        from sklearn import svm
        self.clf = svm.SVC(gamma=0.001, C=100.)
    def classify(self, data, target):
        self.clf.fit(data, target)
    def predict(self, data):
        return self.gnb.predict(data)


data = list(DictReader(open("pbp-2014.csv", 'r')))
pbp2014 = PbpExtractor()
#feature, target = pbp2014.extract(data)
svmClassifer = svmClassifier()
svmClassifer.classify(feature, target)
#y_pred = svmClassifer.predict(feature)
#print("Number of mislabeled points out of a total %d points : %d" % (len(target),(target != y_pred).sum()))
