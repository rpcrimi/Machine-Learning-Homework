
from csv import DictReader, DictWriter
from extractor import PbpExtractor

class Classifier:
    def classify(self):
        y_pred = 1
        return y_pred

class BayesClassifier(Classifier):
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
pbp2014 = PbpExtractor()
feature, target = pbp2014.extract(data)
byClassifer = BayesClassifier()
byClassifer.classify(feature, target)
y_pred = byClassifer.predict(feature)
print("Number of mislabeled points out of a total %d points : %d" % (len(target),(target != y_pred).sum()))
