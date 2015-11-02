from random import randint, seed
from collections import defaultdict
from math import atan, tan, sin, cos, pi, degrees, radians

from numpy import array
from numpy.linalg import norm

from bst import BST

import numpy
import operator
from itertools import combinations
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

kSIMPLE_DATA = [(1., 1.), (2., 2.), (3., 0.), (4., 2.)]
drawSlopes = []
drawRectangles = [[(float('inf'),float('inf')),(float('inf'),float('inf'))]]


class Classifier:
    def correlation(self, data, labels):
        """
        Return the correlation between a label assignment and the predictions of
        the classifier

        Args:
          data: A list of datapoints
          labels: The list of labels we correlate against (+1 / -1)
        """
        assert len(data) == len(labels), \
            "Data and labels must be the same size %i vs %i" % \
            (len(data), len(labels))

        assert all(x == 1 or x == -1 for x in labels), "Labels must be binary"
        corr = 0.0
        for i in range(len(labels)):
            if self.classify(data[i]) == True:
                corr += labels[i]
            else:
                corr -= labels[i]

        return corr / len(labels)


class PlaneHypothesis(Classifier):
    """
    A class that represents a decision boundary.
    """

    def __init__(self, x, y, b):
        """
        Provide the definition of the decision boundary's normal vector

        Args:
          x: First dimension
          y: Second dimension
          b: Bias term
        """
        self._vector = array([x, y])
        self._bias = b

    def __call__(self, point):
        return self._vector.dot(point) - self._bias

    def classify(self, point):
        return self(point) >= 0

    def __str__(self):
        return "x: x_0 * %0.2f + x_1 * %0.2f >= %f" % \
            (self._vector[0], self._vector[1], self._bias)


class OriginPlaneHypothesis(PlaneHypothesis):
    """
    A class that represents a decision boundary that must pass through the
    origin.
    """
    def __init__(self, x, y):
        """
        Create a decision boundary by specifying the normal vector to the
        decision plane.

        Args:
          x: First dimension
          y: Second dimension
        """
        PlaneHypothesis.__init__(self, x, y, 0)


class AxisAlignedRectangle(Classifier):
    """
    A class that represents a hypothesis where everything within a rectangle
    (inclusive of the boundary) is positive and everything else is negative.

    """
    def __init__(self, start_x, start_y, end_x, end_y):
        """

        Create an axis-aligned rectangle classifier.  Returns true for any
        points inside the rectangle (including the boundary)

        Args:
          start_x: Left position
          start_y: Bottom position
          end_x: Right position
          end_y: Top position
        """
        assert end_x >= start_x, "Cannot have negative length (%f vs. %f)" % \
            (end_x, start_x)
        assert end_y >= start_y, "Cannot have negative height (%f vs. %f)" % \
            (end_y, start_y)

        self._x1 = start_x
        self._y1 = start_y
        self._x2 = end_x
        self._y2 = end_y

    def classify(self, point):
        """
        Classify a data point

        Args:
          point: The point to classify
        """
        return (point[0] >= self._x1 and point[0] <= self._x2) and \
            (point[1] >= self._y1 and point[1] <= self._y2)

    def __str__(self):
        return "(%0.2f, %0.2f) -> (%0.2f, %0.2f)" % \
            (self._x1, self._y1, self._x2, self._y2)


class ConstantClassifier(Classifier):
    """
    A classifier that always returns true
    """

    def classify(self, point):
        return True


def constant_hypotheses(dataset):
    """
    Given a dataset in R2, return an iterator over the single constant
    hypothesis possible.

    Args:
      dataset: The dataset to use to generate hypotheses

    """
    yield ConstantClassifier()


def origin_plane_hypotheses(dataset):
    """
    Given a dataset in R2, return an iterator over hypotheses that result in
    distinct classifications of those points.

    Classifiers are represented as a vector.  The classification decision is
    the sign of the dot product between an input point and the classifier.

    Args:
      dataset: The dataset to use to generate hypotheses

    """
    slopes = []
    angleToPoint = [90]
    vectors = []
    # REORDER DATASET IN DESCENDING ANGLES
    l = [(key, degrees(atan(key[1]/key[0]))) for key in dataset]
    l.sort(key=operator.itemgetter(1), reverse=True)
    dataset = [key[0] for key in l]
    for vec in dataset:
        x = vec[0]
        y = vec[1]
        angle = degrees(atan(y/x))

        if angle not in angleToPoint:
            alpha = angle + (angleToPoint[-1]-angle)/2
            angleToPoint.append(angle)
            slope = tan(radians(alpha))
            slopes.append(slope)
            drawSlopes.append(slope)
            y = slope*x
            dx = x
            dy = y
            vectors.append([[-dy, dx], [dy, -dx]])

    for v in vectors:
        for posneg in v:
            yield OriginPlaneHypothesis(posneg[0], posneg[1])


def plane_hypotheses(dataset):
    """
    Given a dataset in R2, return an iterator over hypotheses that result in
    distinct classifications of those points.

    Classifiers are represented as a vector and a bias.  The classification
    decision is the sign of the dot product between an input point and the
    classifier plus a bias.

    Args:
      dataset: The dataset to use to generate hypotheses

    """

    # Complete this for extra credit
    return


def axis_aligned_hypotheses(dataset):
    """
    Given a dataset in R2, return an iterator over hypotheses that result in
    distinct classifications of those points.

    Classifiers are axis-aligned rectangles

    Args:
      dataset: The dataset to use to generate hypotheses
    """
    validRectangles = [[(float('inf'),float('inf')),(float('inf'),float('inf'))]]
    xTree = BST()
    yTree = BST()
    ydataset = [(point[1],point[0]) for point in dataset]
    [xTree.insert(point) for point in dataset]
    [yTree.insert(point) for point in ydataset]

    for i in range(1,len(dataset)+1):
        d = combinations(dataset, i)
        l = []
        for comb in d:
            min_x = min(comb, key=operator.itemgetter(0))[0]
            max_x = max(comb, key=operator.itemgetter(0))[0]
            min_y = min(comb, key=operator.itemgetter(1))[1]
            max_y = max(comb, key=operator.itemgetter(1))[1]
            xRange = []
            yRange = []
            # Generate list of points in each range (x,y)
            for r in xTree.range(min_x, max_x):
                xRange.append(r.key)
            for r in yTree.range(min_y, max_y):
                point = r.key
                yRange.append((point[1], point[0]))

            # Check for points in both ranges
            bothHave = []
            for point in xRange:
                if point in yRange and point not in bothHave:
                    bothHave.append(point)

            # Valid only if length of combination == length of points both have
            if len(comb) == len(bothHave):

                validRectangles.append([(min_x-0.1, min_y-0.1), (max_x+0.1, max_y+0.1)])
                drawRectangles.append(validRectangles[-1])
    
    for vr in validRectangles:
        yield AxisAlignedRectangle(vr[0][0], vr[0][1], vr[1][0], vr[1][1])        

def coin_tosses(number, random_seed=0):
    """
    Generate a desired number of coin tosses with +1/-1 outcomes.

    Args:
      number: The number of coin tosses to perform

      random_seed: The random seed to use
    """
    if random_seed != 0:
        seed(random_seed)

    return [randint(0, 1) * 2 - 1 for x in xrange(number)]


def rademacher_estimate(dataset, hypothesis_generator, num_samples=500,
                        random_seed=0):
    """
    Given a dataset, estimate the rademacher complexity

    Args:
      dataset: a sequence of examples that can be handled by the hypotheses
      generated by the hypothesis_generator

      hypothesis_generator: a function that generates an iterator over
      hypotheses given a dataset

      num_samples: the number of samples to use in estimating the Rademacher
      correlation
    """
    maxCorrelations = []
    for i in range(num_samples):
        correlations = []

        if random_seed != 0:
            coinTosses = coin_tosses(len(dataset), random_seed + i)
        else:
            coinTosses = coin_tosses(len(dataset))
        hyps = hypothesis_generator(dataset)
        for h in hyps:
            correlations.append(h.correlation(dataset, coinTosses))

        maxCorrelations.append(max(correlations))
        i += 1
        drawSlopes = []
        slopes = []

    return sum(maxCorrelations)/float(len(maxCorrelations))

if __name__ == "__main__":

    print("Rademacher correlation of constant classifier %f" %
          rademacher_estimate(kSIMPLE_DATA, constant_hypotheses))
    print("Rademacher correlation of rectangle classifier %f" %
          rademacher_estimate(kSIMPLE_DATA, axis_aligned_hypotheses))
    print("Rademacher correlation of plane classifier %f" %
          rademacher_estimate(kSIMPLE_DATA, origin_plane_hypotheses))

    x = [x[0] for x in kSIMPLE_DATA]
    y = [y[1] for y in kSIMPLE_DATA]
    f, ax = plt.subplots()
    ax.scatter(x, y)
    x = numpy.linspace(0, 5, 10)
    for slope in drawSlopes:
        y = slope*x
        ax.plot(x,y)

    for rect in drawRectangles:
        ax.add_patch(Rectangle((rect[0][0],rect[0][1]), (rect[1][0]-rect[0][0]), (rect[1][1]-rect[0][1]), fill=False))
    ax.set_ylim([-1, 5])
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    plt.show()
