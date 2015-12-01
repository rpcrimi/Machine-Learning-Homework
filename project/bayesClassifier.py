from nflClassifier import *

class BayesClassifier(classifier):
    def __init__(self):
        from sklearn.naive_bayes import GaussianNB
        self.clf = GaussianNB()
