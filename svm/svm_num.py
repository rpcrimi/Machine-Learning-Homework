import argparse
import numpy as np
from sklearn import svm
from collections import defaultdict

class Nums:
    """
    Class to store MNIST data
    """

    def __init__(self, location):
        # You shouldn't have to modify this class, but you can if
        # you'd like.

        import cPickle, gzip

        # Load the dataset
        f = gzip.open(location, 'rb')
        train_set, valid_set, test_set = cPickle.load(f)

        self.train_x, self.train_y = train_set
        self.test_x, self.test_y = valid_set
        f.close()

def show(image):
    """
    Render a given numpy.uint8 2D array of pixel data.
    """
    from matplotlib import pyplot
    import matplotlib as mpl
    fig = pyplot.figure()
    ax = fig.add_subplot(1,1,1)
    imgplot = ax.imshow(image, cmap=mpl.cm.Greys)
    imgplot.set_interpolation('nearest')
    ax.xaxis.set_ticks_position('top')
    ax.yaxis.set_ticks_position('left')
    pyplot.show()

def confusion_matrix(classifier, test_x, test_y):
    """
    Given a matrix of test examples and labels, compute the confusion
    matrix for the current classifier. Should return a dictionary of
    dictionaries where d[ii][jj] is the number of times an example
    with true label ii was labeled as jj.
    :param test_x: Test data representation
    :param test_y: Test data answers
    """
    d = defaultdict(dict)
    data_index = 0
    for example, answer in zip(test_x, test_y):
        label = classifier.predict(example)[0]
        d[answer][label] = d[answer].get(label, 0) + 1
        data_index += 1
        if data_index % 100 == 0:
            print("%i/%i for confusion matrix" % (data_index, len(test_x)))
    return d

def accuracy(conf_matrix):
    """
    Given a confusion matrix, compute the accuracy of the underlying classifier.
    """

    total = 0
    correct = 0
    for i in conf_matrix:
        total += sum(conf_matrix[i].values())
        correct += conf_matrix[i].get(i, 0)

    if total:
        return float(correct) / float(total)
    else:
        return 0.0

def main():

	parser = argparse.ArgumentParser(description='KNN classifier options')
	parser.add_argument('--limit', type=int, default=-1, help="Restrict training to this many examples")
	parser.add_argument('--kernel', type=str, default='rbf', help="Specifies the kernel type to be used in the algorithm. It must be one of "
                             "'linear', 'poly', 'rbf', 'sigmoid', 'precomputed'. Default is 'rbf'.")
	parser.add_argument('--C', type=int, default=1, help="Regularization Parameter")
	args = parser.parse_args()

	data = Nums("../data/mnist.pkl.gz")

	train_X = []
	train_Y = []
	test_X = []
	test_Y = []
	for i in range(len(data.train_y)):
		if data.train_y[i] in (3, 8):
			train_X.append(data.train_x[i])
			train_Y.append(data.train_y[i])


	for i in range(len(data.test_y)):
		if data.test_y[i] in (3, 8):
			test_X.append(data.test_x[i])
			test_Y.append(data.test_y[i])

	SVM = svm.SVC(C=args.C, kernel=args.kernel)
	SVM.fit(train_X[:args.limit], train_Y[:args.limit])

	confusion = confusion_matrix(SVM, test_X, test_Y)
	print("\t" + "\t".join(str(x) for x in [3, 8]))
	print("".join(["-"] * 30))
	for ii in [3, 8]:
		print("%i:\t" % ii + "\t".join(str(confusion[ii].get(x, 0)) for x in [3, 8]))
	print("Accuracy: %f" % accuracy(confusion))

	for ind in range(10):
		new = np.reshape(train_X[ind], (28, 28))
		show(new)

if __name__ == "__main__":
	main()