

class Wrapper:

    def __init__(self, key):
        self._key = key

    def __lt__(self, other):
        return self._key < other._key

def wrapper_lt(a, b):
	return a._key < b._key


pyflate_list = [Wrapper(i) for i in pyflate_list_raw]

