class Wordscovered(object):
    """ Bitmap - emulated with an integer - to keep track 
        of the positions of the already translated words.  
    """
    def __init__(self, _len=0, _covered=0):
        """ _len: number of words covered.
            _covered: bitmap (integer).
        """
        self._len = _len
        self._covered = _covered

    def __eq__(self, other):
        return self._covered == other._covered

    def __len__(self):
        """ Number of words covered. """
        return self._len

    def setPos(self, L):
        """ Set individual bits in the positions specified by L. """
        self._len += len(L)
        for pos in L:
            self._covered |= 1 << pos

    def copy(self):
        """ Returns a copy instance with the same attributes' values. """
        return Wordscovered(self._len, self._covered)

    def hasOverlap(self, start, end):
        """ Check if there is a bit set within this range. """
        t = self._covered                
        t >>= start
        for k in range(end - start):
            if t & 1 == 1: return 1
            t >>= 1
        return 0
    
        
