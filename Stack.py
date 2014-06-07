from Hypothesis import Hypothesis
from heapq import heappush, heappop, nsmallest, nlargest, heapify
from math import log

class Stack(object):
    """ Priority queue for the stack decoding heuristic. 
        We call it "Stack" just to be compatible with the 
        name of the algorithm.
    """

    def __init__(self, threshold=40, percentage=0.001):
        """ Args: 
              threshold: define maximum length of priority queue.
        """
        self.stack = []
        self.threshold = threshold
        self.percentage = log(percentage)
        self.MAX = -100000

    def __getitem__(self, index):
        """ Return only the hypothesis object. The value of 
            ordering should be invisible.
        """
        return self.stack[index][1]

    def __contains__(self, hypothesis):
        """ Override membership operation to search for the tuple 
            (score, hypothesis).
        """
        for h in self.stack:
            if h[1] == hypothesis: return True
        return False

    def __len__(self):
        return len(self.stack)

    def __iter__(self):
        for s in self.stack:
            yield s[1]
    
    def index(self, hypothesis):
        """ If a hypothesis exists, return its position, else -1. """
        for pos, h in enumerate(self.stack):
            if h[1] == hypothesis: return pos
        return -1

    def add(self, hypothesis):
        """ Add a hypothesis element in the stack. 
            If it already exists recombine them by updating the score.
        """
        newelement = (hypothesis.score, hypothesis)
        pos = self.index(hypothesis)
        if pos < 0:
            heappush(self.stack, newelement)
            self.MAX = max(self.MAX, hypothesis.score)
        else:
            if self.stack[pos][1].score < hypothesis.score:
                self.stack.pop(pos)
                heapify(self.stack)
                heappush(self.stack, newelement)
                self.MAX = max(self.MAX, hypothesis.score)


    def nsmallest(self, n=-1):
        """ Generator to the n smallest elements in the queue. If not 
            specified returns them all in increasing order.
        """
        if n < 0: n = len(self.stack)
        for k in nsmallest(n, self.stack):
            yield k[1]

    def nlargest(self, n=-1):
        """ Generator to the n largest elements in the queue. If not 
            specified returns them all in decreasing order.
        """
        if n < 0: n = len(self.stack)
        for k in nlargest(n, self.stack):
            yield k[1]

    def debug(self):
        for k in nlargest(len(self.stack), self.stack):
            print "Key=%f, Score=%f, Output=%s" % (k[0], k[1].score, k[1].output)        

    def prune(self):
        """ Stack pruning. """
        if len(self.stack) > self.threshold:
            toremove = heappop(self.stack)

        while abs(self.MAX - self.stack[0][1].score) > abs(self.percentage):
            heappop(self.stack)
