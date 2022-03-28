# probably needs a better name and some structure.. eventually.
# for now, will use this file to drop misc experimental helper functions
import random
from Sorters import Sorter_Adaptive, Sorter_BottomUp, Sorter_LibraryMethods


def sort_random_input(input_size, sorter_init, k=2, seed=72, test_mode=False):
    # make a random input of the desired length
    random.seed(seed)
    random_input = list(range(input_size))
    random.shuffle(random_input)

    # sort it with the desired input and settings
    sorter = sorter_init(random_input, k, test_mode)
    sorter.sort()


# usage guide

# current best sorter - bottom up adaptive sorter using the loser tree
# sort_random_input(100000, Sorter_Adaptive.Sorter_PingPong_Adaptive, k=4, seed=101)

# sorter using loser tree, but no run detection
# sort_random_input(100000, Sorter_BottomUp.Sorter_PingPong_BottomUp, k=4, seed=101)

# sorter using list.sort - a good guide to how to make wrapper classes for other sorters, if you prefer that to using
#   the interface directly
# sort_random_input(100000, Sorter_LibraryMethods.Sorter_Default)

