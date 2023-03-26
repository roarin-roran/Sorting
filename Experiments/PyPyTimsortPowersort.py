import random
import pandas as pd
import matplotlib.pylab as plt

import PyPySorters.listsort_powersort as powersort
import PyPySorters.listsort_timsort as timsort
import Support.Counters as Counters
import Inputs.Inputs as Inputs
import Inputs.util as util


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
        diff['mc'] = 1.0*ts['mc'] / ps['mc'] if ps['mc'] > 0 else math.nan
        diff['cmps'] = 1.0*ts['cmps'] / ps['cmps'] if ps['cmps'] > 0 else math.nan
        diff['mc-diff'] = 1.0 * ts['mc'] - ps['mc']
        diff['cmps-diff'] = 1.0 * ts['cmps'] - ps['cmps']
        diff['mc-powersort'] = ps['mc']
        diff['cmps-powersort'] = ps['cmps']
        diff['input-hash'] = ps['input-hash']
        diffs = diffs.append(diff, ignore_index=True)
    return diffs


def contest(input_generator,
            reps=100, n=10000, seed=2348905734,
            print_describe=True,
            describe_percentiles=[0.01, .25, .5,],
            show_histograms=False,
            show_scatter=True,
            return_diffs=False,
            ):
    print('Running  ...')
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
        plt.scatter('mc', 'cmps', data = diffs, marker='x', )
        plt.show()
    return diffs if return_diffs else None


def bad_input(n, RNG):
    sqrtn = int(n ** 0.5)
    lst = [0] * n
    Inputs.fill_with_asc_runs_same(lst,
                                   Inputs.exponential_random_run_lengths(n, sqrtn, RNG),
                                   1, use_n_as_last_entry=False)
    lst = util.rank_reduce_ties_desc(lst)
    return lst


def find_bad_inputs(n=10000, seed=2348905734):
    RNG = random.Random(seed)
    worst_badness = 0
    worst_input = []
    last_input = None
    def next_input():
        nonlocal last_input
        last_input = bad_input(n, RNG)
        return last_input
    try:
        while True:
            diffs = differences(1, next_input)
            badness = diffs['cmps'][0]
            # print(badness)
            if badness > worst_badness:
                worst_badness = badness
                worst_input = last_input
                print(worst_badness)
    except KeyboardInterrupt:
        print(worst_input)


# contest(lambda n, rand: Inputs.random_permutation(n, rand), reps=10,n=100)


if 0:
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

    contest(input_generator)


find_bad_inputs(10000)
