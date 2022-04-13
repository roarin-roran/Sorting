from Merger_IPQs import MergerIPQ
import math


class MergerIPQ_LoserTree(MergerIPQ.MergerIPQ):
    """an ipq using a loser tree, a restricted binary heap which is arguably a tournament tree variation (opinions
    differ in the literature)"""
    # todo - update to use binary heap language in method names, variable names, and comments

    def __init__(self, initial_priorities, option_code=2, test_mode=False):
        super().__init__(initial_priorities, option_code, test_mode)

        self.n = len(initial_priorities)

        # initialise with all elements at equal priorities
        self.priorities = [-math.inf] * self.n
        self.loser_tree = list(range(self.n))

        # repeatedly update the leading element, so the -inf's will rise to the top
        for input_number in range(self.n):
            updating = self.loser_tree[0]
            self.update_lowest_priority(initial_priorities[updating])

    def update_lowest_priority(self, new_priority: int) -> None:
        """updates the lowest priority element per the loser tree, and sinks the modified element as far as necessary"""
        self.priorities[self.loser_tree[0]] = new_priority

        # first node only has one child - special case it
        posn = 0
        keep_sinking = self._first_larger(0, 1)
        if keep_sinking:
            self._swap_nodes(0, 1)
            posn = 1

        while keep_sinking:
            left_child = 2 * posn
            right_child = left_child + 1

            # default to the left child, for simplicity
            favoured_child = left_child

            both_children_valid = right_child < self.n
            if both_children_valid:
                if self._first_larger(left_child, right_child):
                    favoured_child = right_child
                # else use default value
            else:
                # test if neither child is valid
                left_child_valid = left_child < self.n
                if not left_child_valid:
                    keep_sinking = False

            # if we're still going, test current node against favoured child and sink if possible.
            if keep_sinking:
                if self._first_larger(posn, favoured_child):
                    self._swap_nodes(posn, favoured_child)
                    posn = favoured_child
                else:
                    keep_sinking = False

    def _first_larger(self, first_index, second_index) -> bool:
        """returns true if the first valid tournament index is larger, false otherwise. """
        # if the challenger is larger on priority
        if self.priorities[self.loser_tree[first_index]] > self.priorities[self.loser_tree[second_index]]:
            return True
        # if the defender  wins on priority
        elif self.priorities[self.loser_tree[first_index]] < self.priorities[self.loser_tree[second_index]]:
            return False
        # if both players have the same priority, return the smallest run to ensure stability
        else:
            if first_index > second_index:
                return True
            else:
                return False

    def _swap_nodes(self, first_index, second_index):
        """swaps two nodes in the loser tree"""
        temp = self.loser_tree[first_index]
        self.loser_tree[first_index] = self.loser_tree[second_index]
        self.loser_tree[second_index] = temp

    def peek_at_lowest_priority_element(self) -> (int, int):
        """returns the (index, priority) of the top element of the loser tree"""
        return self.loser_tree[0], self.priorities[self.loser_tree[0]]
