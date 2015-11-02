from csv import DictReader, DictWriter

import numpy as np
from numpy import array
import nltk
import pprint
import argparse
import operator
from nltk.corpus import wordnet as wn
from nltk.util import ngrams
from collections import defaultdict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier

kTARGET_FIELD = 'spoiler'
kTEXT_FIELD   = 'sentence' 
kTAGSET       = ["", "True", "False"]
def accuracy(classifier, x, y, examples):
    predictions = classifier.predict(x)
    cm = confusion_matrix(y, predictions)

    print("Accuracy: %f" % accuracy_score(y, predictions))

    print("\t".join(kTAGSET[1:]))
    for ii in cm:
        print("\t".join(str(x) for x in ii))

def example(sentence):
    sentence = sentence.split()
    for position in range(0, len(sentence)):
        word = sentence[position]
        ex = word

        if position > 0:
            prev = " P:%s" % sentence[position - 1]
        else:
            prev = ""

        if position < len(sentence) - 1:
            next = " N:%s" % sentence[position + 1]
        else:
            next = ''

        all_before = " " + " ".join(["B:%s" % x
                                     for x in sentence[:position]])
        all_after = " " + " ".join(["A:%s" % x
                                    for x in sentence[(position + 1):]])

        dictionary = ["D:ADJ"] * len(wn.synsets(word, wn.ADJ)) + \
          ["D:ADV"] * len(wn.synsets(word, wn.ADV)) + \
          ["D:VERB"] * len(wn.synsets(word, wn.VERB)) + \
          ["D:NOUN"] * len(wn.synsets(word, wn.NOUN))

        dictionary = " " + " ".join(dictionary)

        char = ' '
        padded_word = "~%s^" % sentence[position]
        for ngram_length in xrange(2, 5):
            char += ' ' + " ".join("C:%s" % "".join(cc for cc in x)
                                   for x in ngrams(padded_word, ngram_length))
        ex += char
        ex += prev
        ex += next
        ex += all_after
        ex += all_before
        ex += dictionary
    return ex

def prune(sentence):
    splitSentence = [word for word in sentence.upper().split()]
    #tokenized = nltk.pos_tag(splitSentence)
    newSentence = []
    for i in range(0, len(splitSentence)):
        word        = splitSentence[i]
        word_after  = splitSentence[i+1]
        word_before = splitSentence[i-1]
        all_before  = splitSentence[:i]
        all_after   = splitSentence[i:]

    return " ".join(newSentence)

class Analyzer:
    def __init__(self, word, before, after, prev, next, char, dict):
        self.word = word
        self.after = after
        self.before = before
        self.prev = prev
        self.next = next
        self.dict = dict
        self.char = char

    def __call__(self, feature_string):
        feats = feature_string.split()

        if self.word:
            yield feats[0]

        if self.after:
            for ii in [x for x in feats if x.startswith("A:")]:
                yield ii
        if self.before:
            for ii in [x for x in feats if x.startswith("B:")]:
                yield ii
        if self.prev:
            for ii in [x for x in feats if x.startswith("P:")]:
                yield ii
        if self.next:
            for ii in [x for x in feats if x.startswith("N:")]:
                yield ii
        if self.dict:
            for ii in [x for x in feats if x.startswith("D:")]:
                yield ii
        if self.char:
            for ii in [x for x in feats if x.startswith("C:")]:
                yield ii

class Featurizer:
    def __init__(self, analyzer):
        self.vectorizer = TfidfVectorizer(analyzer=analyzer)

    def train_feature(self, examples):
        #return self.vectorizer.fit_transform(examples)
        return self.vectorizer.fit_transform([example(e) for e in examples])

    def test_feature(self, examples):
        #return self.vectorizer.transform(examples)
        return self.vectorizer.transform([example(e) for e in examples])

    def show_top10(self, classifier, categories):
        feature_names = np.asarray(self.vectorizer.get_feature_names())
        if len(categories) == 2:
            top10 = np.argsort(classifier.coef_[0])[-20:]
            bottom10 = np.argsort(classifier.coef_[0])[:20]
            print("Pos: %s" % " ".join(feature_names[top10]))
            print("Neg: %s" % " ".join(feature_names[bottom10]))
        else:
            for i, category in enumerate(categories):
                top10 = np.argsort(classifier.coef_[i])[-20:]
                print("%s: %s" % (category, ",".join(feature_names[top10])))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--word', default=False, action='store_true',
                        help="Use word features")
    parser.add_argument('--all_before', default=False, action='store_true',
                        help="Use all words before context as features")
    parser.add_argument('--all_after', default=False, action='store_true',
                        help="Use all words after context as features")
    parser.add_argument('--one_before', default=False, action='store_true',
                        help="Use one word before context as feature")
    parser.add_argument('--one_after', default=False, action='store_true',
                        help="Use one word after context as feature")
    parser.add_argument('--characters', default=False, action='store_true',
                        help="Use character features")
    parser.add_argument('--dictionary', default=False, action='store_true',
                        help="Use dictionary features")

    flags = parser.parse_args()

    analyzer = Analyzer(flags.word, flags.all_before, flags.all_after,
                        flags.one_before, flags.one_after, flags.characters,
                        flags.dictionary)

    # Cast to list to keep it all in memory
    train = list(DictReader(open("../data/spoilers/train.csv", 'r')))
    test = list(DictReader(open("../data/spoilers/test.csv", 'r')))
    feat = Featurizer(analyzer)

    labels = []
    for line in train:
        if not line[kTARGET_FIELD] in labels:
            labels.append(line[kTARGET_FIELD])

    print("Label set: %s" % str(labels))

    x_train = feat.train_feature(x[kTEXT_FIELD] for x in train)
    x_test = feat.test_feature(x[kTEXT_FIELD] for x in test)

    y_train = array(list(labels.index(x[kTARGET_FIELD])
                         for x in train))

    print(len(train), len(y_train))
    print(set(y_train))

    # Train classifier
    lr = SGDClassifier(loss='log', penalty='l2', shuffle=True)
    lr.fit(x_train, y_train)

    feat.show_top10(lr, labels)

    predictions = lr.predict(x_test)
    o = DictWriter(open("predictions.csv", 'w'), ["id", "spoiler"])
    o.writeheader()
    for ii, pp in zip([x['id'] for x in test], predictions):
        d = {'id': ii, 'spoiler': labels[pp]}
        o.writerow(d)

    accuracy(lr, x_train, y_train, [example(e[kTEXT_FIELD]) for e in train])
