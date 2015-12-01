from csv import DictReader, DictWriter

from extractor import NewPbpExtractor
from nflEvaluation import *
from nflClassifier import *

from sklearn.cross_validation import train_test_split

#--------------------------------------------------#
#training
data = list(DictReader(open("pbp-2014.csv", 'r')))
data2014 = list(DictReader(open("pbp-2013.csv", 'r')))
data.extend(data2014)
pbp2014 = NewPbpExtractor()
pbp2014.buildFormationList(data)
feature, target = pbp2014.extract4Classifier(data)

X_train, X_test, y_train, y_test = train_test_split(feature, target, test_size=.2, random_state=42)

#test
#data2015 = list(DictReader(open("pbp-2015.csv", 'r')))
#X_test, y_test = pbp2014.extract4Classifier(data2015)
#--------------------------------------------------#


#--------------------------------------------------#
#BayesClassifier
#clf = BayesClassifier()
#--------------------------------------------------#
#svmClassifier
clf = svmClassifier()
clf.linear()
#clf.gamma()
#--------------------------------------------------#
#KNeighborsClassifier
#clf = knClassifier()
#--------------------------------------------------#
#DecisionTreeClassifier
#clf = dtClassifier()
#--------------------------------------------------#
#RandomForestClassifier
#clf = rfClassifier()
#--------------------------------------------------#
#AdaBoostClassifier
#clf = adaBoostClassifier()
#--------------------------------------------------#


clf.classify(X_train, y_train)
temp = clf.predict(X_test)
y_pred = clf.recommendation(temp)
#--------------------------------------------------#
print("Number of a total %d points" % len(y_test) )
class2014 = classifierEvaluation()
print class2014.Score(y_test, y_pred)