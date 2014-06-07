from collections import defaultdict
from Wordscovered import Wordscovered
from Phrasetable import Phrasetable
from Hypothesis  import Hypothesis
from Stack import Stack
import sys

class Decoder(object):

    def __init__(self, sentence, phrasefile, ordering="monotonic", histogram=40, percentage=0.001):
        """ Args:
                sentence: sentence to be decoded
                phrasefile: filename with phrases corpus
                ordering: reordering to choose "monotonic" (default)
                          or "unlimited".
                histogram: threshold for stack size pruning.
                percentage: threshold for pruning the worst hypotheses in the 
                            stack in comparison with the best.            
        
            Creates a phrases lookup with start-end 
            positions and their translations with respective scores.
        """
        self.sentence     = sentence
        self.length       = len(sentence.split())
        self.stacks       = [Stack(histogram, percentage) for i in range(self.length + 1)]  
        self.phraselookup = defaultdict(dict)

        self.expand       = self.expand_monotonic
        if ordering == "unlimited":
            self.expand = self.expand_unlimited

        # Load translation options into memory.
        ptable = Phrasetable()
        ptable.loadTable(phrasefile)
        self.MAXLEN = ptable.MAXLEN
        for i in ptable.lookup_opt(sentence):
            self.phraselookup[i[0]][i[1]] = i[2]

    def decode(self):
        """ Fill the stacks by generating translations left-to-right. """
        self.stacks[0].add(Hypothesis(Wordscovered())) # add empty hypothesis
        for stack in self.stacks:
            for hypo in stack:
                self.expand(hypo)

    def constructHypo(self, hypo, score, english, start, end):
        """ Construct a new hypothesis by updating the score, its 
            output and coverage.
        """  
        new_score   = hypo.score  + score
        new_output  = hypo.output + " " + english
        new_wordscovered = hypo.wordscovered.copy()
        new_wordscovered.setPos(range(start,end))
        return Hypothesis(new_wordscovered, new_score, new_output)

    def expand_unlimited(self, hypo):
        """ Expand a hypothesis - unlimited reordering. """
        if len(hypo) == 0: start = 0
        else: start = len(hypo)
        
        for start, rest in self.phraselookup.iteritems():
            for end in rest:
                if not hypo.wordscovered.hasOverlap(start, end):
                    for english, score in self.phraselookup[start][end].iteritems():    
                        new_hypo = self.constructHypo(hypo, score, english, start, end)   
                        self.stacks[len(new_hypo)].add(new_hypo)
                        self.stacks[len(new_hypo)].prune()

    def expand_monotonic(self, hypo):
        """ Expand a hypothesis - monotonic way. """

        # Monotonic: start from (hypo_end + 1)
        if len(hypo) == 0: start = 0
        else: start = len(hypo)

        for end in range(start+1, self.length+1):
            if end not in self.phraselookup[start]:
                continue

            for english, score in self.phraselookup[start][end].iteritems():                
                new_hypo = self.constructHypo(hypo, score, english, start, end)   
                self.stacks[len(new_hypo)].add(new_hypo)
                self.stacks[len(new_hypo)].prune()
        
