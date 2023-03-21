import random
import pandas as pd
import matplotlib.pylab as plt

import PyPySorters.listsort_powersort
import PyPySorters.listsort_timsort
import Support.Counters as Counters
import Inputs.Inputs as Inputs



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
    diffs = pd.DataFrame(columns=['algo', 'mc', 'cmps', 'input-hash'])
    for _ in range(repetitions):
        A = input_generator()
        ps = cost(A, PyPySorters.listsort_powersort)
        ts = cost(A, PyPySorters.listsort_timsort)
        diff = {}
        diff['algo'] = 'timsort-powersort'
        diff['mc'] = 1.0 * ts['mc'] - ps['mc']
        diff['cmps'] = 1.0 * ts['cmps'] - ps['cmps']
        diff['input-hash'] = ps['input-hash']
        diffs = diffs.append(diff, ignore_index=True)
    return diffs



n = 10000
sqrtn = int(n ** 0.5)
reps = 10


RNG = random.Random(2348905734)
diffs = differences(reps, lambda: Inputs.random_runs(n, sqrtn, RNG))
# print(diffs)
print(diffs['mc']  .describe(percentiles=[0.01, 0.05, 0.1, .25, .5, .75]))
print(diffs['cmps'].describe(percentiles=[0.01, 0.05, 0.1, .25, .5, .75]))


RNG = random.Random(2348905734)
diffs = differences(reps, lambda: Inputs.random_permutation(n, RNG))
# print(diffs)
print(diffs['mc']  .describe(percentiles=[0.01, 0.05, 0.1, .25, .5, .75]))
print(diffs['cmps'].describe(percentiles=[0.01, 0.05, 0.1, .25, .5, .75]))
