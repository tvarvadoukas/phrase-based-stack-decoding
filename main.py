# MT Assignment 2
# Curtis Holmes, Riaz Moola, Theo Varvadoukas

import sys
from Decoder import Decoder

def usage():
    print "Usage: python %s <phrase table> <ordering (optional)> <stack_size_threshold (optional)> <percentage_threshold (optional)>" % (sys.argv[0]) 
    print '\t<ordering>: can be either "monotonic" (default) or "unlimited"'
    print '\t<stack_size_threshold>: integer - upper limit for the size of the stack (default=40)'
    print '\t<percentage_threshold>: float number <1 - for threshold pruning (default=0.001)' 
    print ""
    print 'E.g. 1: python %s toy.phrases.txt unlimited' % (sys.argv[0])
    print 'E.g. 2: python %s toy.phrases.txt unlimited 80 0.2' % (sys.argv[0])

if len(sys.argv) < 2:
    usage()
    sys.exit(1)

# Defaults.
table = sys.argv[1]
ordering = "monotonic"
stack_size = 40
perc = 0.001

if len(sys.argv) >= 3:
    ordering = sys.argv[2]

if len(sys.argv) >= 4:
    stack_size = int(sys.argv[3])
     
if len(sys.argv) == 5:
    perc = float(sys.argv[4])

s = "das ist ein kleines haus"
d = Decoder(s, table, ordering, stack_size, perc)
d.decode()

for id, s in enumerate(d.stacks):
    print "Stack_%d = %d | " % (id, len(s)),
print ""

for pos, hypo in enumerate(d.stacks[-1].nlargest()):
    print "%d\t%s\t\t%f" % (pos, hypo.output, hypo.score)
