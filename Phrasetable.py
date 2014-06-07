from collections import defaultdict

class Phrasetable(object):

    def __init__(self):
        """ pt: phrasetable as a dictionary of dictionaries 
                (Foreign [tuple] - English [string]). 
            MAXLEN: maximum source length
        """
        self.pt = defaultdict(dict)
        self.MAXLEN = 0

    def loadTable(self, filename):
        """ Load phrases mapping into the table. 
            Line format: <foreign> ||| <english> ||| <score>
        """
        with open(filename, "r") as F:
            for line in F:
                line    = line.split("|||")
                source  = tuple(line[0].split())
                foreign = line[1].strip()
                score   = float(line[2]) 
                self.pt[source][foreign] = score

                self.MAXLEN = max(self.MAXLEN, len(source))
                
    def lookup(self, sentence):
        """ Lookup sentence's ngrams in the phrasetable and 
            print their score.
        """
        sentence = sentence.split() 
        length = len(sentence)

        notfound = "%d..%d nothing found"

        for i in range(length):
            for j in range(i + 1, length + 1):
                ngram  = tuple(sentence[i:j])
                curlen = len(ngram) 

                if curlen > self.MAXLEN:
                    print notfound % (i, j)
                    continue

                if ngram not in self.pt:
                    print notfound % (i, j)
                    continue

                print "%d..%d found %d" % (i, j, len(self.pt[ngram]))
                for english, score  in self.pt[ngram].iteritems():
                    print "%s ||| %f" % (english, score)

    def lookup_opt(self, sentence):
        """ Lookup sentence's ngrams. Same as above but optimized 
            (no printing necessary). Yields a tuple of 
            (start_position, end_position, {translation, score}). 
        """
        sentence = sentence.split() 
        length = len(sentence)

        for i in range(length):
            for j in range(i + 1, length + 1):
                ngram  = tuple(sentence[i:j])
                curlen = len(ngram) 

                if curlen > self.MAXLEN:
                    break

                if ngram not in self.pt:
                    continue

                for english, score  in self.pt[ngram].iteritems():
                    yield (i, j, self.pt[ngram])




if __name__ == "__main__":
    # Load phrase table.
    ptable = Phrasetable() 
    ptable.loadTable("toy.phrases.txt")
    ptable.lookup("das ist ein kleines haus")
