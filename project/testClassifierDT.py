from csv import DictReader, DictWriter
import numpy as np
from itertools import product

from extractor import NewPbpExtractor
from nflEvaluation import classifierEvaluation
from nflClassifier import *
from sklearn.cross_validation import train_test_split


#--------------------------------------------------#
#training
#data2: combine 2014, first 80% for train, 20% for test
data2013 = list(DictReader(open("pbp-2013.csv", 'r')))
data2014 = list(DictReader(open("pbp-2014.csv", 'r')))
data2015 = list(DictReader(open("pbp-2015.csv", 'r')))
dataList = [data2013, data2014, data2015]
dataName = ["2013","2014","2015"]

o = DictWriter(open("DecisionTreeClassifier.csv", 'w'), ["dataName", "classifier", "percent", "score", "OmniScore", "Type1-A/A/Good","Type2-A/B/Bad",  "Type3-A/B/Good", "Type4-A/A/Bad"])
o.writeheader()

#---------------------------------#
for dataindex in range(len(dataList)):
    pbp2014 = NewPbpExtractor()
    pbp2014.buildFormationList(dataList[dataindex])
    feature, target = pbp2014.extract4Classifier(dataList[dataindex])

    dataLength = feature.shape[0]
    dataLength80 = round(dataLength * 0.8)
    X_train = feature[0:dataLength80,:]
    X_test = feature[(dataLength80+1):dataLength,:]
    y_train = target[0:dataLength80]
    y_test = target[(dataLength80+1):dataLength]


    class2014 = classifierEvaluation()

    Bscore, Bnum, BtypeNum, BomniScore = class2014.Score(y_test, y_test)
    baseline = {'dataName': dataName[dataindex] ,'classifier': 'baseline', 'percent': Bscore/float(BomniScore),'score': Bscore,'OmniScore': BomniScore, 'Type1-A/A/Good': BtypeNum[0], 'Type2-A/B/Bad': BtypeNum[1], 'Type3-A/B/Good': BtypeNum[2], 'Type4-A/A/Bad': BtypeNum[3]}
    o.writerow(baseline)

    #--------------------------------------------------#
    clf = []
    max_depth = np.linspace(5, 13, num = 13-5+1)
    splitter = ["best", "random"]
    max_features = np.linspace(7, 16, num = 16-7+1)
    criterion = ["gini", "entropy"]
    algorithm = ["SAMME", "SAMME.R"]
    method = ["dt", "svm"]

    algorithmForkn = ["ball_tree", "brute", "auto"]
    n_neighbors  = np.linspace(3, 8, num = 8-3+1)
    metric = ["minkowski", "euclidean", "manhattan", "chebyshev"]

    C = [.0001, .001, .01, .1, 1, 10, 100, 1000]
    kernel = ["linear", "poly", "rbf", "sigmoid", "precomputed"]

    #DecisionTreeClassifier
    for a, b, c in product(max_depth, splitter, max_features):
        clf.append( dtClassifier(max_depth=a, splitter=b, max_features=int(c)) )


    for i in range(len(clf)):
        clf[i].classify(X_train, y_train, needWeight=False)
        temp = clf[i].predict(X_test)
        y_pred = clf[i].recommendation(temp)

        score, num, typeNum, omniScore = class2014.Score(y_test, y_pred)

        clfCVS = {'dataName': dataName[dataindex], 'classifier': clf[i].name, 'percent': score/float(omniScore),'score': score,'OmniScore': omniScore, 'Type1-A/A/Good': typeNum[0], 'Type2-A/B/Bad': typeNum[1], 'Type3-A/B/Good': typeNum[2], 'Type4-A/A/Bad': typeNum[3]}
        o.writerow(clfCVS)
