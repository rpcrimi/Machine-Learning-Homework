from csv import DictReader, DictWriter

from extractor import NewPbpExtractor
from nflEvaluation import classifierEvaluation
from nflClassifier import *
from sklearn.cross_validation import train_test_split


#--------------------------------------------------#
#training
#---------------------------------#
#data1: combine 2014 and 2013
#data = list(DictReader(open("pbp-2014.csv", 'r')))
#data2014 = list(DictReader(open("pbp-2013.csv", 'r')))
#data.extend(data2014)
#---------------------------------#
#data2: combine 2014, first 80% for train, 20% for test
data = list(DictReader(open("pbp-2014.csv", 'r')))
#---------------------------------#
pbp2014 = NewPbpExtractor()
pbp2014.buildFormationList(data)
feature, target = pbp2014.extract4Classifier(data)

#X_train, X_test, y_train, y_test = train_test_split(feature, target, test_size=.2, random_state=42)

dataLength = feature.shape[0]
dataLength80 = round(dataLength * 0.8)
#dataLength20 = dataLength - dataLength80
#X_train = np.zeros((dataLength80, feature.shape[1]))
#X_test = np.zeros((dataLength20, feature.shape[1]))
#y_train = np.zeros(dataLength80)
#y_test = np.zeros(dataLength20)
X_train = feature[0:dataLength80,:]
X_test = feature[(dataLength80+1):dataLength,:]
y_train = target[0:dataLength80]
y_test = target[(dataLength80+1):dataLength]


#test
#data2015 = list(DictReader(open("pbp-2015.csv", 'r')))
#X_test, y_test = pbp2014.extract4Classifier(data2015)
#--------------------------------------------------#


#--------------------------------------------------#
#BayesClassifier
#clf = BayesClassifier()
#--------------------------------------------------#
#svmClassifier
#clf = svmClassifier()
#clf.linear()
#clf.gamma()
#--------------------------------------------------#
#KNeighborsClassifier
#clf = knClassifier()
#--------------------------------------------------#
#DecisionTreeClassifier
clf = dtClassifier()
#--------------------------------------------------#
#RandomForestClassifier
#clf = rfClassifier()
#--------------------------------------------------#
#AdaBoostClassifier
#clf = adaBoostClassifier()
#--------------------------------------------------#

clf.classify(X_train, y_train, needWeight=False)
temp = clf.predict(X_test)
y_pred = clf.recommendation(temp)
#--------------------------------------------------#
class2014 = classifierEvaluation()
score, num, typeNum, omniScore = class2014.Score(y_test, y_pred)
print("Number of a total %d points, Score %d, percent %f" % (len(y_test), score, score/float(omniScore)) )
print("Number of a each type")
print typeNum
