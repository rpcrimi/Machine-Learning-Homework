from csv import DictReader, DictWriter
import numpy as np
from itertools import product

from extractor import NewPbpExtractor
from nflEvaluation import classifierEvaluation
from nflClassifier import *
from sklearn.cross_validation import train_test_split

mc = 10
#--------------------------------------------------#
#training
#data2: combine 2014, first 80% for train, 20% for test
data2013 = list(DictReader(open("pbp-2013.csv", 'r')))
data2014 = list(DictReader(open("pbp-2014.csv", 'r')))
data2015 = list(DictReader(open("pbp-2015.csv", 'r')))
dataList = [data2013, data2014, data2015]
dataName = ["2013","2014","2015"]

o = DictWriter(open("rfClassifier-mc.csv", 'w'), ["dataName", "classifier", "percent", "score", "OmniScore", "Type1-A/A/Good","Type2-A/B/Bad",  "Type3-A/B/Good", "Type4-A/A/Bad"])
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

    clf.append(rfClassifier())
    for a, b, c in product(max_depth, criterion, max_features):
        clf.append( rfClassifier(max_depth=a, criterion=b, max_features=int(c)) )


    for i in range(len(clf)):
        scoreTotal = 0
        omniScoreTotal = 0
        typeNum1 = 0
        typeNum2 = 0
        typeNum3 = 0
        typeNum4 = 0
        for j in range(mc):
            clf[i].classify(X_train, y_train, needWeight=False)
            temp = clf[i].predict(X_test)
            y_pred = clf[i].recommendation(temp)

            score, num, typeNum, omniScore = class2014.Score(y_test, y_pred)

        scoreTotal += score/float(mc)
        omniScoreTotal += omniScore/float(mc)
        typeNum1 += typeNum[0]/float(mc)
        typeNum2 += typeNum[1]/float(mc)
        typeNum3 += typeNum[2]/float(mc)
        typeNum4 += typeNum[3]/float(mc)

        clfCVS = {'dataName': dataName[dataindex], 'classifier': clf[i].name, 'percent': score/float(omniScore),'score': score,'OmniScore': omniScore, 'Type1-A/A/Good': typeNum1, 'Type2-A/B/Bad': typeNum2, 'Type3-A/B/Good': typeNum3, 'Type4-A/A/Bad': typeNum4}
        o.writerow(clfCVS)
