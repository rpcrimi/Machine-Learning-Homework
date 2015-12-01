from nflClassifier import *

class svmClassifier(classifier):
    def __init__(self):
        from sklearn import svm
        self.clf = svm.SVC(gamma=0.001, C=100.)
