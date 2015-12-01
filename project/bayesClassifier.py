from nflClassifier import *

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
