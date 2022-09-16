""" 
Compare the performance of variants of Complete Greedy algorithm on uniformly-random integers.
Aims to reproduce the results of Korf, Moffitt and Schreiber (2018), JACM paper.
Author: Erel Segal-Halevi
Since:  2022-06
"""

from typing import Callable
import numpy as np, prtpy
from prtpy import objectives as obj
from splitting import splitting

TIME_LIMIT=30

def partition_random_items(
    numbins: int,
    numitems: int,
    bitsperitem: int,
    rangeitems: float,
    distribution: np.random.mtrand.RandomState,
    instance_id: int, # dummy parameter, to allow multiple instances of the same run
    **kwargs
):
    largest_item = 2**bitsperitem-1
    items = np.array( distribution(rangeitems * largest_item + 1, largest_item, numitems), dtype=np.int64)
    perfect = sum(items)/numbins
    result = []
    for i in range(numbins):
        sums = prtpy.partition(
            algorithm=splitting,
            numbins=numbins,
            items=items, 
            splits=i,
            outputtype=prtpy.out.Sums,
            time_limit=TIME_LIMIT,
            **kwargs
        )
        minmax = max(sums)
        result.append({
            'split' : i,
            'minmax' : minmax
        })
        if minmax == perfect:
            break
    return {
        "minmaxes": result
    }


if __name__ == "__main__":
    import logging, experiments_csv
    experiments_csv.logger.setLevel(logging.INFO)
    experiment = experiments_csv.Experiment("results/", "amount_of_splitting.csv", backup_folder=None)

    prt = prtpy.partitioning
    input_ranges = {
        "numbins": [2],
        "numitems": [10, 12, 14],
        "bitsperitem": [16],
        "rangeitems": [0,0.5],
        "distribution": [np.random.randint, np.random.normal],
        "instance_id": range(10),
    }
    experiment.run_with_time_limit(partition_random_items, input_ranges, time_limit=TIME_LIMIT)