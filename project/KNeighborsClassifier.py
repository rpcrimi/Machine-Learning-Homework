from nflClassifier import *

class knClassifier(classifier):
    def __init__(self):
        from sklearn.neighbors import KNeighborsClassifier
        self.clf = KNeighborsClassifier(3)
