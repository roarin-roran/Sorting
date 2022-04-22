# probably needs a better name and some structure.. eventually.
# for now, will use this file to drop misc experimental helper functions
from random import Random
from Sorters import Sorter_Adaptive, Sorter_BottomUp, Sorter_LibraryMethods, Sorter_Peeksort


# From main repo repository run
# pypy3 -m pyperf timeit --rigorous -v -s 'import Experiments.Experiments as exp' 'exp.run_bottom_up(n=1000000, repetitions=1, k=2)'

# pypy3 -m pyperf timeit --rigorous -v  -s  'import Experiments' 'run()'

# on ben's uni laptop:
# in:
#   C:\Users\sgbsmit5\PycharmProjects\Sorting
# run:
#   C:\Users\sgbsmit5\pypy3.9-v7.3.9-win64\pypy3 -m pyperf timeit --rigorous -v  -s  "import Experiments.Experiments" "Experiments.Experiments.run()"

# on ben's home PC:
# in:
#   C:\Users\carri\Documents\GitHub\Sorting>
# run:
#   C:\Users\carri\pypy\pypy -m pyperf timeit --rigorous -v  -s  "import Experiments.Experiments" "Experiments.Experiments.run_bottom_up(10000, 1, 4)"


def sort_random_input(input_size, sorter, repetitions=100, k=2, seed=72, test_mode=False):
    # make a random input of the desired length
    random = Random()
    random.seed(seed)
    random_input = list(range(input_size))

    for x in range(repetitions):
        random.shuffle(random_input)

        # sort it with the desired input and settings
        sorter.sort(random_input, k=k)


# usage guide

def run_peeksort(n=100000, repetitions=1, k=4, seed=86438564):
    sort_random_input(n, Sorter_Peeksort, repetitions=repetitions, k=k, seed=seed)


def run_adaptive(n=100000, repetitions=1, k=4, seed=86438564):
    sort_random_input(n, Sorter_Adaptive, repetitions=repetitions, k=k, seed=seed)


def run_bottom_up(n=100000, repetitions=1, k=4, seed=86438564):
    sort_random_input(n, Sorter_BottomUp, repetitions=repetitions, k=k, seed=seed)

# current best sorter - bottom up adaptive sorter using the loser tree
# sort_random_input(100000, Sorter_Adaptive.Sorter_PingPong_Adaptive, k=4, seed=101)


# sort_random_input_2(100000, Sorter_Adaptive, repetitions=10, k=4, seed=101)
# sort_random_input_2(100000, Sorter_LibraryMethods, repetitions=10, k=4, seed=101)


# sorter using loser tree, but no run detection
# sort_random_input(100000, Sorter_BottomUp.Sorter_PingPong_BottomUp, k=4, seed=101)

# sorter using list.sort - a good guide to how to make wrapper classes for other sorters, if you prefer that to using
#   the interface directly
# sort_random_input(100000, Sorter_LibraryMethods.Sorter_Default)
