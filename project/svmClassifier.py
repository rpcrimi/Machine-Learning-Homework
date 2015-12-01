from nflClassifier import *

class svmClassifier(classifier):
    def __init__(self):
        from sklearn import svm
        self.clf = svm.SVC(gamma=0.001, C=100.)
    def classify(self, data, target):
        self.clf.fit(data, target)
    def predict(self, data):
        return self.clf.predict(data)
