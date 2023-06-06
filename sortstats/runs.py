import math
from collections import Counter


def runs(lst):
    """
    input: list, which should probably have some runs added to it
    output: list of ranges of all runs
    """
    
    ranges = []
    start_index = 0
    last_num = lst[0]
    increasing = None
    
    for i in range(1, len(lst)):
        # initialise or switch
        if increasing is None:
            increasing = lst[i] >= last_num
        # if the direction changes, record and start a new run
        elif increasing != (lst[i] >= last_num):
            end_index = i
            ranges.append((start_index, end_index, increasing))
            start_index = i
            increasing = None
        last_num = lst[i]
        
    end_index = len(lst)
    ranges.append((start_index, end_index, increasing))
    return ranges


def run_lengths(ranges):
    # _ used here to ignore the variable "increasing"
    return [end - start for start, end, _ in ranges]


def entropy(lst):
    n = sum(lst)
    entropy = 0
    for x in lst:
        entropy += x * math.log2(n/x)
    return entropy / n




if __name__ == "__main__":
    print(runs([1, 2, 3, 3, 2, 1, 1, 3, 4, 5, 6, 5, 4, 3, 6, 5]))
    print(run_lengths(runs([1, 2, 3, 3, 2, 1, 1, 3, 4, 5, 6, 5, 4, 3, 6, 5])))



from time import time
from random import randint


class Value:
    comparisons = 0

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        Value.comparisons += 1
        return self.value < other.value

    def __repr__(self):
        return repr(self.value)


if __name__ == '__main__':

    n = 3000
    while True:
        for MAX in (10, 500, 1000, 2000, 10_000, 100_000, 1_000_000):
            data = n * sorted([randint(1, MAX) for _ in range(n)], reverse=True)
            # data = [x for _ in range(n) for x in sorted([randint(1, MAX) for _ in range(n)], reverse=True)]
            # data = list(map(Value, data))
            H_dup = entropy(data)
            H_run = entropy(run_lengths(runs(data)))
            Value.comparisons = 0
            start = time()
            answer = sorted(data)
            end = time()
            comparisons = Value.comparisons
            print(f'{len(data)=} {len(set(data))=} {comparisons=} {MAX=}', '\ttime =',
                  end - start, '\tH_dup =', H_dup, '\tH_run =', H_run)
