import math
import random

import pandas as pd

# add parent folder to path
import sys
sys.path.append('..')

import Inputs.Inputs as Inputs
import Inputs.util as util
import PyPySorters.listsort_powersort as powersort
import PyPySorters.listsort_timsort as timsort
import Support.Counters as Counters


def cost(lst, sorter):
    wrapped = [Counters.ComparisonCounter(x) for x in lst]
    Counters.reset_counters()
    sorter.sort(wrapped)
    assert Counters.ComparisonCounter.EQ_COMPARISONS == 0
    return {
        'algo': sorter.name(),
        'mc': Counters.MergeCosts.MERGECOST,
        'cmps': Counters.ComparisonCounter.COMPARISONS,
        'input-hash': hash(tuple(lst)),
    }


def differences(repetitions, input_generator):
    diffs = pd.DataFrame()
    for i in range(repetitions):
        if repetitions > 1:
            print(i)
        A = input_generator()
        ps = cost(A, powersort)
        ts = cost(A, timsort)
        diff = {}
        diff['iteration'] = i
        diff['algo'] = 'timsort-over-powersort'
        diff['mc'] = 1.0 * ts['mc'] / ps['mc'] if ps['mc'] > 0 else math.nan
        diff['cmps'] = 1.0 * ts['cmps'] / ps['cmps'] if ps['cmps'] > 0 else math.nan
        diff['mc-diff'] = 1.0 * ts['mc'] - ps['mc']
        diff['cmps-diff'] = 1.0 * ts['cmps'] - ps['cmps']
        diff['mc-powersort'] = ps['mc']
        diff['cmps-powersort'] = ps['cmps']
        diff['input-hash'] = ps['input-hash']
        diffs = diffs.append(diff, ignore_index=True)
    return diffs


def bad_input(n, RNG):
    sqrtn = int(n ** 0.5)
    lst = [0] * n
    Inputs.fill_with_asc_runs_same(lst,
                                   Inputs.exponential_random_run_lengths(n, sqrtn, RNG),
                                   1, use_n_as_last_entry=False)
    lst = util.rank_reduce_ties_desc(lst)
    return lst


def find_bad_inputs(n=10000, seed=2348905734, badness_criterion='cmps',
                    output_file='bad_inputs.txt'):
    RNG = random.Random(seed)
    min_badness = 100
    worst_badness = 0
    worst_input = []
    last_input = None

    def next_input():
        nonlocal last_input
        last_input = bad_input(n, RNG)
        return last_input

    while True:
        diffs = differences(1, next_input)
        badness = diffs[badness_criterion][0]
        # print(badness)
        min_badness = min(min_badness, badness)
        if badness > worst_badness:
            worst_badness = badness
            worst_input = last_input
            print(worst_badness, min_badness)
            with open(output_file, 'w') as f:
                f.write('# cmps:{}\t mc:{}\n'.format(diffs['cmps'][0], diffs['mc'][0]))
                f.write('# worst_{}:{}\t min_{}:{}\n'.format(badness_criterion, worst_badness, badness_criterion, min_badness))
                f.write('bad_{}_{} = '.format(badness_criterion, n) + str(worst_input))
                f.write('\n')
                f.flush()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("usage: python FindBadInputs.py <badness_criterion> <n> <seed> [-f]")
        exit(1)
    badness_criterion = sys.argv[1]
    n = int(sys.argv[2])
    seed = int(sys.argv[3])
    print("finding bad input for n={}, seed={}, badness_criterion={}"
          .format(n, seed, badness_criterion))
    filename = "bad_{}_n={}_seed={}.py".format(badness_criterion, n, seed)
    # abort if exists
    import os
    if os.path.exists(filename):
        if len(sys.argv) >= 4 and sys.argv[4] == '-f':
            print("file {} already exists, overwriting".format(filename))
        else:
            print("file {} already exists, aborting".format(filename))
            exit(1)
    find_bad_inputs(n, seed, badness_criterion, filename)
