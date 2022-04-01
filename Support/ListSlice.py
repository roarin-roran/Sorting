class ListSlice:
    """holds a subset of a list in a light way with few safety measures. stores a pointer to the original list, and
    the start and end of the desired subset"""
    def __init__(self, sliced_list, start, end):
        self.list = sliced_list
        self.start = start
        self.end = end

    def __str__(self):
        return str(self.list[self.start:self.end])

    def get_list(self):
        return self.list[self.start:self.end]
