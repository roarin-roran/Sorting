# Running time comparisons between Timsort and Powersort
# Intended to be run under CPython 3.11 compiled with either Timsort or Powersort
# as obtained from https://github.com/sebawild/cpython using branch 3.11-instrumented
#
# Instructions for compilation:
# 1. Clone the repository and checkout the branch 3.11-instrumented:
#    git clone https://github.com/sebawild/cpython.git
#    git checkout 3.11-instrumented
# 2. Select the sorting method in Objects/listobject.c (lines 12 onwards):
#    - Timsort: #define USE_TIMSORT
#    - Powersort: #define USE_POWERSORT
#    (At any time, only one of the two must be defined!)
#    - For running time tests, also remove #define PRINT_INFO
# 3. Compile CPython with the following command:
#    ./configure --enable-optimizations
#    make
#    make test
# 4. (optional) Create a venv for the compiled CPython:
#    ./python -m venv venv
#    source venv/bin/activate
#    Check the version of Python:
#    python --version

#
#    python3 -m pip install -r requirements.txt

# 5. Run the script:
#    python PyConRunningTimes.py
#    (or ./python PyConRunningTimes.py if you are not using a venv)
#


import timeit
import random
import sys
sys.path.append('..')

print('Running time comparison')

import Inputs.Inputs as Inputs
import Inputs.Books as Books
import Inputs.bad_examples as bad_examples
import Inputs.bad_cmps_1m as bad_cmps_1m

seed = 2378956239523
n = 1000000


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

def wrap_list(lst):
    return [f"{x:0100d}" for x in lst]

# runner = pyperf.Runner()
# don't use pyperf for now; separate process makes things complicated
results = []
for name, input_generator in inputs:
    print(f"Running {name} ...")
    lst = input_generator()
    lst = wrap_list(lst)
    # Take time using pyperf
    # time = runner.timeit('sorted(lst)', globals=globals())
    times = timeit.repeat('sorted(lst)', globals=globals(), number=200, repeat=5)
    # times = [timeit.timeit('sorted(lst)', globals=globals(), number=1)]
    for i, time in enumerate(times):
        results.append((name, i, time))

# Print results
for name, i, time in results:
    # print as table
    print(f"{name}\t{i}\t{time}")
