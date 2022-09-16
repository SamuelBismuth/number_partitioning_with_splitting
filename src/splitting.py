from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, printbins
from prtpy.binners import BinnerKeepingContents, BinnerKeepingSums, Binner
import logging

from prtpy.partitioning.integer_programming import optimal

BinsArray = Any

def splitting(
    binner: Binner,
    numbins: int,
    items: List[Any],
    splits: int=0,
    method: Any=optimal,
    **kwargs
):
    '''
    >>> from prtpy.binners import BinnerKeepingContents, BinnerKeepingSums
    >>> from prtpy.partitioning import greedy   
    >>> from prtpy.partitioning.integer_programming import optimal
    >>> myitems = [1830164603,1501606828,2896223917,1418696650,3010882753,1614975677,2222323474,2951314428, 717964778, 14336094]
    >>> printbins(splitting(BinnerKeepingContents(), 2, items=myitems, splits=1, method=optimal, time_limit=10))
    Bin #0: [2951314428, 2222323474, 1614975677, 717964778, 14336094, 1568330150.0], sum=9089244601.0
    Bin #1: [2896223917, 1830164603, 1501606828, 1418696650, 1442552603.0], sum=9089244601.0
    
    >>> printbins(splitting(BinnerKeepingContents(), 2, items=[1,2,3,3,5,9,9], splits=1, method=greedy.greedy))
    Bin #0: [9, 2, 1, 4.0], sum=16.0
    Bin #1: [5, 3, 3, 5.0], sum=16.0
    
    >>> printbins(splitting(BinnerKeepingContents(), 2, items=[1,2,3,3,5,9,9], splits=1, method=greedy.greedy))
    Bin #0: [9, 2, 1, 4.0], sum=16.0
    Bin #1: [5, 3, 3, 5.0], sum=16.0

    >>> printbins(splitting(BinnerKeepingContents(), 3, items=[1,2,3,3,5,9,9], splits=1, method=greedy.greedy))
    Bin #0: [9, 1.666666666666666], sum=10.666666666666666
    Bin #1: [5, 2, 3.666666666666666], sum=10.666666666666666
    Bin #2: [3, 3, 1, 3.666666666666666], sum=10.666666666666666
    
    >>> printbins(splitting(BinnerKeepingContents(), 3, items=[1,2,3,3,5,9,9], splits=1, method=greedy.greedy))
    Bin #0: [9, 1.666666666666666], sum=10.666666666666666
    Bin #1: [5, 2, 3.666666666666666], sum=10.666666666666666
    Bin #2: [3, 3, 1, 3.666666666666666], sum=10.666666666666666

    >>> printbins(splitting(BinnerKeepingContents(), 3, items=[1,2,3,3,5,9,9], splits=2, method=greedy.greedy))
    Bin #0: [5, 5.666666666666666], sum=10.666666666666666
    Bin #1: [3, 2, 5.666666666666666], sum=10.666666666666666
    Bin #2: [3, 1, 6.666666666666666], sum=10.666666666666666

    >>> myitems = [221601401843059,118938948724098,184253429347216,29233828957338, 91456159593160, 74233669065147, 117427553028646, 194140418207739, 119113612016846, 254887462258969, 135258993363461, 233050030199667, 251680500108416, 138798065968236, 189501698875220, 201333312136263, 87366706683415, 37283760168354, 114752638983718, 224947602971898, 183924496164875, 27132967553073, 250241987637910, 213987654648338, 236264787046065, 238398341371687, 112804135553193, 244465002633195, 104078556205908, 279271625289745, 99733973893767, 148786775664782, 256005893684184, 224185518377716, 30549521555485, 248844308110135, 157109277063655, 66114220156242, 99866451688792, 194017776723049, 109500646882469, 187809609054884, 219507475463816, 42470105339308, 104730236733168]
    >>> printbins(splitting(BinnerKeepingContents(), 3, items=myitems, splits=2, method=greedy.greedy))
    Bin #0: [254887462258969, 238398341371687, 236264787046065, 219507475463816, 201333312136263, 189501698875220, 183924496164875, 135258993363461, 118938948724098, 112804135553193, 99866451688792, 99733973893767, 42470105339308, 37283760168354, 27132967553073, 169046802731161.5], sum=2366353712332102.5
    Bin #1: [251680500108416, 244465002633195, 233050030199667, 221601401843059, 194140418207739, 194017776723049, 184253429347216, 138798065968236, 117427553028646, 109500646882469, 104730236733168, 91456159593160, 66114220156242, 30549521555485, 184568749352355.5], sum=2366353712332102.5
    Bin #2: [250241987637910, 248844308110135, 224947602971898, 224185518377716, 213987654648338, 187809609054884, 157109277063655, 148786775664782, 119113612016846, 114752638983718, 104078556205908, 87366706683415, 74233669065147, 29233828957338, 181661966890412.5], sum=2366353712332102.5
    '''
    items.sort()
    items = items[::-1]
    entire_items = items[splits:]
    split_items = items[:splits]
    logging.debug('hello')
    bins = method(binner, numbins, entire_items, **kwargs)
    logging.debug('hello2')
    bins = add_split_items(binner, numbins, sum(split_items), sum(items)/numbins, bins)
    logging.debug('entire_items: {0}'.format(entire_items))
    logging.debug('split_items: {0}'.format(split_items))
    logging.debug('bins: {0}'.format(binner))
    return bins


def add_split_items(
    binner: Binner,
    numbins: int,
    split_items: int,
    average: float, 
    bins: BinsArray
):
    '''
    Add the split items
    '''
    overflow = 0
    overflowed_bins = 0
    for ibin in range(numbins):
        if binner.sums(bins)[ibin] > average:
            overflow += binner.sums(bins)[ibin] - average
            overflowed_bins += 1
    
    overflow = overflow / (numbins - overflowed_bins)

    logging.debug('average: {0}'.format(average))
    logging.debug('bins.sums: {0}'.format(binner.sums(bins)))
    logging.debug('overflow: {0}'.format(overflow))

    for ibin in range(numbins):
        # If every bin is smaller than the average, there exists a perfect solution.
        # Then, divide the split-items to increase every bin under the average to average - (overflow / bins.num)
        if binner.sums(bins)[ibin] < average:
            split_item = (average - overflow) - binner.sums(bins)[ibin]
            split_items -= split_item
            binner.add_item_to_bin(bins, split_item, ibin)

    logging.info("split_items={0}".format(split_items))

    assert int(split_items) == 0.0

    return bins
   

if __name__ == "__main__":
    import doctest

    # splitting(BinnerKeepingContents(), 2, items=[1,2,3,3,5,9,9], splits=1, method=greedy)

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))