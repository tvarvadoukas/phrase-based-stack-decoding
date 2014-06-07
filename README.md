phrase-based-stack-decoding
===========================

Phrase based stack decoding for machine translation. 


The implementation is consisted of five main classes each one of them 
implemented in its own file:

Wordscovered
Hypothesis
Phrasetable
Stack
Decoder

Wordscovered
---------------
Wordcovered is a bitmap which is emulated for space efficiency as an integer. 
When the word is partially translated the respective bit is set. This also 
speeds up a lot the comparison of two bitmaps which is just the comparison 
of two small integers. In case we were using a list it would need a complexity 
of O(sentence_length) each time. 

Hypothesis
--------------
Hypothesis is a class that contains the current output, its score and a 
Wordscovered instance. We have also defined an equality operator which 
considers two hypotheses being equal when they have translated the same 
foreign words with the exactly the same words. Score is left out and is 
handled by another class for the case of hypotheses recombination.

Phrasetable
-------------
Class that loads fast the phrases table into memory. They are stored in a 
dictionary of dictionaries of the form {start:{end:{english, score}}}. This 
allows O(1) lookup to start retrieving pairs in the range [start, end].

Stack
-------
Stack is being implemented as a priority queue (minheap) due to the many pops 
O(logn)and lookups O(1) of the minimum element. The disadvantage is searching 
an element in the queue linearly which can be easily resolved by keeping a parallel 
dictionary. 

A more efficient implementation would use the dictionary as 
the main data structure for storing hypotheses and the priority queue to 
pop very fast the minimum element when requested. Under this implementation 
we would achieve searching in O(1), insertion O(1) for the dictionary and O(logn) 
for the priority queue and deletion again O(1) for the dictionary and O(logn) for 
the priority queue. The space complexity would be doubled but it is small even for
an average sentence of around 10 words and a stack size of 80 entries, therefore 
the space-time trade-off would make sense. However, we prefered to keep things 
simple for readability purposes and keep a clean code that shows the concept clearly. 

Decoder
----------
The decoder after loading the phrases table into memory starts expanding each hypothesis 
in each stack. For the monotonic case we generate [start, end] pairs very quickly and 
check if we have a translation option for this range. On the other hand, for the 
unlimited case instead of trying to generate all possible ranges (and their permutations), 
we do the inverse and iterate over the phrase table instead and check if a translation option 
is valid (i.e. if there is no overlap with the current hypothesis). 

Pruning
We have included also implementations for histogram and threshold pruning for each stack that 
can be set from the command line as well. 

Running the program
python main.py <phrase table> <ordering (optional)> <stack_size_threshold (optional)> <percentage_threshold (optional)>
	<ordering>: can be either "monotonic" (default) or "unlimited"
	<stack_size_threshold>: integer - upper limit for the size of the stack (default=60)
	<percentage_threshold>: float number <1 - for threshold pruning (default=0.001)

E.g. 1: python main.py toy.phrases.txt unlimited
Description: Runs the decoding for the phrase table in "toy.phrases.txt" with unlimited 
reordering and default values of 60 for histogram and 0.001 for threshold pruning.

E.g. 2: python main.py toy.phrases.txt unlimited 80 0.2
Description: Runs the decoding for the phrase table in "toy.phrases.txt" with unlimited 
reordering and values of 80 for histogram and 0.2 for threshold pruning.
