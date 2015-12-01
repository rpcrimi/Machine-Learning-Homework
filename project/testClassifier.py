from csv import DictReader, DictWriter

from extractor import NewPbpExtractor
from nflEvaluation import *

#--------------------------------------------------#
#training
data = list(DictReader(open("pbp-2014.csv", 'r')))
data2014 = list(DictReader(open("pbp-2013.csv", 'r')))
data.extend(data2014)
pbp2014 = NewPbpExtractor()
pbp2014.buildFormationList(data)
feature, target = pbp2014.extract4Classifier(data)
#test
#data2015 = list(DictReader(open("pbp-2015.csv", 'r')))
data2015 = list(DictReader(open("pbp-2014.csv", 'r')))
feature2015, target2015 = pbp2014.extract4Classifier(data2015)
#--------------------------------------------------#


#--------------------------------------------------#
#BayesClassifier
from bayesClassifier import BayesClassifier
byClassifer = BayesClassifier()
byClassifer.classify(feature, target)

temp = byClassifer.predict(feature2015)
y_pred = byClassifer.recommendation(temp)
#--------------------------------------------------#
'''
#svmClassifier
svmClassifer = svmClassifier()
svmClassifer.classify(feature, target)

temp = svmClassifer.predict(feature2015)
y_pred = svmClassifer.recommendation(temp)
'''
#--------------------------------------------------#

print("Number of a total %d points" % len(target2015) )
class2014 = classifierEvaluation()
print class2014.Score(target2015, y_pred)
