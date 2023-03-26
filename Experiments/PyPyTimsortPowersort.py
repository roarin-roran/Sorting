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
    for i in range(repetitions):
        print(i)
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

def contest(input_generator,
            reps=200, n=10000, seed=2348905734,
            print_describe=True,
            describe_percentiles=[0.01, 0.05, 0.1, .25, .5, .75],
            show_histograms=False,
            show_scatter=True,
            ):
    RNG = random.Random(seed)
    diffs = differences(reps, lambda: input_generator(n, RNG))
    if print_describe:
        print(diffs['mc']  .describe(percentiles=describe_percentiles))
        print()
        print(diffs['cmps'].describe(percentiles=describe_percentiles))
        print()
    if show_histograms:
        plt.hist(diffs['mc'])
        plt.show()
        plt.hist(diffs['cmps'])
        plt.show()
    if show_scatter:
        plt.scatter('mc', 'cmps', data = diffs, marker='x')
        plt.show()


# contest(lambda n, rand: Inputs.random_permutation(n, rand), reps=10,n=100)


n = 10000
sqrtn = int(n ** 0.5)
reps = 1

import sortstats.runs as runs
import Inputs.util as util

def input_generator(n, RNG):
    sqrtn = int(n ** 0.5)
    lst = Inputs.random_runs(n, sqrtn, RNG)
    run_lens = runs.run_lengths(runs.runs(lst))
    Inputs.fill_with_asc_runs_same(lst, run_lens, 1)
    return util.rank_reduce(lst)

import cProfile

cProfile.run('contest(input_generator,reps=1)', sort='time')

# contest(input_generator)


# RNG = random.Random(2348905734)
# diffs = differences(reps, lambda: Inputs.random_runs(n, sqrtn, RNG))
# # print(diffs)
# print(diffs['mc']  .describe(percentiles=[0.01, 0.05, 0.1, .25, .5, .75]))
# print(diffs['cmps'].describe(percentiles=[0.01, 0.05, 0.1, .25, .5, .75]))
#
#
# RNG = random.Random(2348905734)
# diffs = differences(reps, lambda: Inputs.random_permutation(n, RNG))
# # print(diffs)
# print(diffs['mc']  .describe(percentiles=[0.01, 0.05, 0.1, .25, .5, .75]))
# print(diffs['cmps'].describe(percentiles=[0.01, 0.05, 0.1, .25, .5, .75]))

