# Running time comparisons between Timsort and Powersort
# Intended to be run under CPython 3.11 compiled with either Timsort or Powersort
# as obtained from https://github.com/sebawild/cpython using branch 3.11-instrumented
#
# For instructions, see PyConRunningTimesPlots.ipynb

import timeit
import random
import sys

sys.path.append('..')

print('Running time comparison')

import Inputs.Inputs as Inputs
import Inputs.Books as Books
import Inputs.bad_examples as bad_examples
import Inputs.bad_cmps_1m as bad_cmps_1m
import Inputs.bad_cmps_1m_2 as bad_cmps_1m_2
import Support.Counters as Counters

seed = 2378956239523
n = 1000000


RNG = random.Random(seed)
inputs = [
    ("bad-example-cmps-1m ", lambda: bad_cmps_1m.bad_cmps_1000000),
    ("bad-example-cmps-1m2", lambda: bad_cmps_1m_2.bad_cmps_1000000),
    ("random-permutations ", lambda: Inputs.random_permutation(n, RNG)),
    ("random-permutations2", lambda: Inputs.random_permutation(n, RNG)),
    ("random-sqrtn-runs   ", lambda: Inputs.random_runs(n, int(n ** 0.5), RNG)),
    ("random-sqrtn-runs2  ", lambda: Inputs.random_runs(n, int(n ** 0.5), RNG)),
    ("random-sqrtn-runs3  ", lambda: Inputs.random_runs(n, int(n ** 0.5), RNG)),
    ("words-of-bible      ", lambda: Books.list_of_words_bible()),
    ("bad-example-cmps    ", lambda: bad_examples.bad_cmps_10k),
    ("bad-example-mc      ", lambda: bad_examples.bad_mc_10k),
]
class ComparisonSlower:

    def __init__(self, obj):
        self.obj = obj


    def __lt__(self, other):
        # waste some time to slow things down
        for i in range(100):
            pass
        return self.obj < other.obj

    def __repr__(self):
        return 'ComparisonSlower(' + repr(self.obj) + ')'

    def __str__(self):
        return 'ComparisonSlower(' + str(self.obj) + ')'


def wrap_list(lst):
    # convert number to string with x digits including leading zeros
    # return ['{:0>100}'.format(x) for x in lst]
    # Counters.reset_counters()
    return [ComparisonSlower(x) for x in lst]


def talk_slides_experiments_april_16_2023():
    global seed, n, sep, lst, RNG, inputs
    seed = 2378956239523
    n = 1000000
    sep = '\t'

    RNG = random.Random(seed)
    inputs = [
        ("bad-example-cmps-1m ", lambda: bad_cmps_1m.bad_cmps_1000000),
        ("random-permutations ", lambda: Inputs.random_permutation(n, RNG)),
        ("random-permutations2", lambda: Inputs.random_permutation(n, RNG)),
        ("random-sqrtn-runs   ", lambda: Inputs.random_runs(n, int(n ** 0.5), RNG)),
        ("random-sqrtn-runs2  ", lambda: Inputs.random_runs(n, int(n ** 0.5), RNG)),
        ("random-sqrtn-runs3  ", lambda: Inputs.random_runs(n, int(n ** 0.5), RNG)),
        ("words-of-bible      ", lambda: Books.list_of_words_bible()),
        ("bad-example-cmps    ", lambda: bad_examples.bad_cmps_10k),
        ("bad-example-mc      ", lambda: bad_examples.bad_mc_10k),
    ]

    # runner = pyperf.Runner()
    # don't use pyperf for now; separate process makes things complicated
    results = []
    for name, input_generator in inputs:
        print(f"Running {name} ...")
        lst = input_generator()
        times = timeit.repeat('sorted(lst)', globals=globals(), number=200, repeat=5)
        for i, time in enumerate(times):
            results.append((name, i, time))

    # Print results
    print('algo', sep, 'i', sep, 'time')
    for name, i, time in results:
        # print as table
        print(f"{name}{sep}{i}{sep}{time}")



# PLAYGROUND

if 1:
    # runner = pyperf.Runner()
    # don't use pyperf for now; separate process makes things complicated
    results = []
    for name, input_generator in inputs:
        print(f"Running {name} ...")
        lst = input_generator()
        # lst = wrap_list(lst)
        # Take time using pyperf
        # time = runner.timeit('sorted(lst)', globals=globals())
        # times = timeit.repeat('sorted(lst)', globals=globals(), number=5, repeat=5)
        times = [timeit.timeit('sorted(lst)', globals=globals(), number=1)]
        # Counters.print_counters()
        for i, time in enumerate(times):
            results.append((name, i, time))

    # Print results
    for name, i, time in results:
        # print as table
        print(f"{name}\t{i}\t{time}")


# talk_slides_experiments_april_16_2023()
