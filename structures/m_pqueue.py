"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.
"""

from typing import Any

from structures.m_entry import *


class PriorityQueue:
    """
    An implementation of the PriorityQueue ADT.
    The provided methods consume keys and values. Keys are called "priorities"
    and should be integers in the range [0, n] with 0 being the highest priority.
    Values are called "data" and store the payload data of interest.
    For convenience, you may wish to also implement the functionality provided in
    terms of the Entry type, but this is up to you.
    """
    
    def __init__(self):
        """
        Construct the priority queue.
        You are free to make any changes you find suitable in this function to initialise your pq.
        """
        self.queue = [None]

    # Warning: This insert() signature changed as of skeleton 1.1, previously
    # the priority and data arguments were switched
    def insert(self, priority: int, data: Any) -> None:
        """
        Insert some data to the queue with a given priority.
        Hint: FIFO queue can just always have the same priority value, no
        need to implement an extra function.
        """
        if self.queue[0] is None:  # If the heap is empty, initialize it
            self.queue[0] = (priority, data)
            return

        self.queue.append((priority, data))  # Append the new element to the end of the list
        self._bubble_up(len(self.queue) - 1)  # Restore the heap property by bubbling up the last element

    def _bubble_up(self, index: int) -> None:
        while index // 2 > 0:  # While the element has a parent
            parent_index = index // 2
            if self.queue[index][0] < self.queue[parent_index][0]:  # If the child has a smaller key than the parent
                self.queue[index], self.queue[parent_index] = self.queue[parent_index], self.queue[index]  # Swap them
            index = parent_index  # Move up the tree

    def insert_fifo(self, data: Any) -> None:
        """
        UPDATE in Skeleton v2.2: Allows a user to add data for FIFO queue
        operations. You may assume a user will NOT mix insert() and
        insert_fifo() - they will either use one all of the time, or the
        other all of the time.
        """
        self.insert(0, data)

    def get_min(self) -> Any:
        """
        Return the highest priority value from the queue, but do not remove it
        """
        if self.is_empty():
            return None
        return self.queue[1][1]  # Return the data of the item with the highest priority without removing it

    def remove_min(self) -> Any:
        """
        Extract (remove) the highest priority value from the queue.
        You must then maintain the queue to ensure priority order.
        """
        if self.is_empty():
            return None
        min_val = self.queue[1][1]  # The root of the heap has the minimum key
        self.queue[1] = self.queue[-1]  # Replace the root with the last element in the list
        self.queue.pop()  # Remove the last element from the list
        if not self.is_empty():
            self._bubble_down(1)  # Restore the heap property by bubbling down the new root
        return min_val

    def _bubble_down(self, index: int) -> None:
        while index * 2 < len(self.queue):  # While the element has at least one child
            min_child_index = self._min_child(index)
            if self.queue[index][0] > self.queue[min_child_index][0]:  # If the child has a smaller key than the parent
                self.queue[index], self.queue[min_child_index] = self.queue[min_child_index], self.queue[
                    index]  # Swap them
            index = min_child_index  # Move down the tree

    def _min_child(self, index: int) -> int:
        if index * 2 + 1 >= len(self.queue):  # If the element has only one child
            return index * 2
        if self.queue[index * 2][0] < self.queue[index * 2 + 1][
            0]:  # Return the index of the child with the smaller key
            return index * 2
        return index * 2 + 1

    def get_size(self) -> int:

        return len(self.queue) - 1 if self.queue[0] is not None else 0

    def is_empty(self) -> bool:

        return self.queue[0] is None or len(self.queue) == 1


# if __name__ == "__main__":
#     import random
#
#     input_list = list(range(1, 100001))  # Create a list of integers from 1 to 100000
#     random.shuffle(input_list)  # Shuffle the list
#     pq = PriorityQueue()
#     for num in input_list:
#         pq.insert(num, num)  # Here, we are using the integers themselves as both the data and the priority
#     output_list = []
#     while not pq.is_empty():
#         output_list.append(pq.remove_min())
#     if output_list == sorted(output_list):
#         print("Test passed: The output list is sorted.")
#     else:
#         print("Test failed: The output list is not sorted. Investigate the issue.")
