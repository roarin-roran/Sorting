class ListSlice:
    def __init__(self, sliced_list, start, end):
        self.list = sliced_list
        self.start = start
        self.end = end

    def __str__(self):
        return str(self.list[self.start:self.end])

    def get_list(self):
        return self.list[self.start:self.end]