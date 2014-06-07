from Wordscovered import Wordscovered

class Hypothesis(object):
    def __init__(self, wordscovered, score=0, output=""):
        """ Args:
                wordscovered: partial translation bitmap.
                score: log-probability of current hypothesis
                output: current output
        """
        self.wordscovered   = wordscovered.copy()
        self.score          = score
        self.output         = output

    def __eq__(self, other):
        """ Equal if cover the same words and have exactly the same  
            translation. 
        """
        return ( (self.wordscovered == other.wordscovered) and 
                 (self.output       == other.output      ) )

    def __len__(self):
        """ Length of hypothesis is the number of words in the partial 
            translation. 
        """
        return len(self.wordscovered)

    def updateScore(self, other):
        """ If two hypotheses are equal then keep the highest 
            score. 
        """
        self.score = max(self.score, other.score)
