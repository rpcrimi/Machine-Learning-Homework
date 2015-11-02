import itertools
import os
import re
import operator
import ast
import matplotlib.pyplot as plt

features           = ["--word", "--all_before", "--all_after", "--one_before", "--one_after", "--characters", "--dictionary" ]
permutatedFeatures = []
accuracy           = []

for i in range(len(features)+1):
  for c in itertools.combinations(features, i):
    permutatedFeatures.append(' '.join(c))

permutatedFeatures.pop(0)
permutatedFeatures.pop(1)
permutatedFeatures.pop(1)
permutatedFeatures.pop(1)
permutatedFeatures.pop(1)
for perm in permutatedFeatures:
	print perm
	os.system("python classify.py %s > output.txt" % perm)
	f = open("output.txt", "r")
	for line in f:
		if re.search("Accuracy:", line):
			accuracy.append(float(line.split()[1]))
			break
	f.close()

for i in range(len(accuracy)):
	print "(%s: %s)" % (permutatedFeatures[i], accuracy[i])

print "*"*50
combinedList = []
for i in range(len(accuracy)):
	combinedList.append((permutatedFeatures[i], accuracy[i]))
sort = sorted(combinedList, key=operator.itemgetter(1))
print sort

perm    = []
values  = []
for v in sort:
	perm.append(v[0])
	values.append(v[1])

fig = plt.figure()
plot = fig.add_subplot(111)
plot.plot(range(len(values)), values)
plot.set_xlabel("Feature Combination")
plot.set_ylabel("Accuracy")
plot.set_title("Accuracy of Each Permutation of Features")
plt.show()