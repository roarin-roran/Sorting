# run as: 
# pypy3 -m pyperf timeit -v  -s 'import pyflate_list' 'pyflate_list.sort_pyflate_list()'
# pypy3 -m pyperf timeit -v  -s 'import pyflate_list' 'pyflate_list.timsort_pyflate_list()'
# pypy3 -m pyperf timeit -v  -s 'import pyflate_list' 'pyflate_list.powersort_pyflate_list()'

# or, if needs be, without pyperf, as:
# python3 -m timeit -s 'import pyflate_list' 'pyflate_list.sort_pyflate_list()'

import listsort_timsort
import listsort_timsort_opt
import listsort_powersort
import listsort_baby
import sys




class Wrapper:

    def __init__(self, key):
        self._key = key

    def __lt__(self, other):
        return self._key < other._key

pyflate_list = [Wrapper(i) for i in pyflate_list_raw]



my_value = 0

def sort_pyflate_list(reps=1):
	#print("Running systemsort")
	res = 0;
	for x in range(reps):
		copy = pyflate_list[:]
		copy.sort()
		res += copy[42]._key
	return res

def timsort_pyflate_list(reps=1):
	res = 0;
	for x in range(reps):
		copy = pyflate_list[:]
		listsort_timsort.sort(copy)
		res += copy[42]._key
	return res

def opttimsort_pyflate_list(reps=1):
	res = 0;
	for x in range(reps):
		copy = pyflate_list[:]
		listsort_timsort_opt.sort(copy)
		res += copy[42]._key
	return res

def powersort_pyflate_list(reps=1):
	res = 0;
	for x in range(reps):
		copy = pyflate_list[:]
		listsort_powersort.sort(copy)
		res += copy[42]._key
	return res

def babysort_pyflate_list(reps=1):
	res = 0;
	for x in range(reps):
		copy = pyflate_list[:]
		listsort_baby.sort(copy)
		res += copy[42]._key
	return res

to_run = {
	"lib": sort_pyflate_list,
	"tim": timsort_pyflate_list,
	"power": powersort_pyflate_list
}


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Pass one of " + str(list(to_run.keys())))
		exit(42)
	to_run[sys.argv[1]]()
