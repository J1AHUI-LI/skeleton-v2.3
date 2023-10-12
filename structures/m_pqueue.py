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
        self._queue = [None]
        self._size = 0

    def _sink(self, k):
        while 2 * k <= self._size:
            j = 2 * k
            if j < self._size and self._queue[j].get_key() > self._queue[j + 1].get_key():
                j += 1
            if not self._queue[k].get_key() > self._queue[j].get_key():
                break
            self._queue[k], self._queue[j] = self._queue[j], self._queue[k]
            k = j

    def insert(self, priority: int, data: Any) -> None:
        """
        Insert some data to the queue with a given priority.
        Hint: FIFO queue can just always have the same priority value, no
        need to implement an extra function.
        """
        entry = Entry(priority, data)
        self._queue.append(entry)
        self._size += 1
        self._swim(self._size)

    def _swim(self, k):
        while k > 1 and self._queue[k // 2].get_key() > self._queue[k].get_key():
            self._queue[k], self._queue[k // 2] = self._queue[k // 2], self._queue[k]
            k = k // 2

    def insert_fifo(self, data: Any) -> None:
        """
        UPDATE in Skeleton v2.2: Allows a user to add data for FIFO queue
        operations. You may assume a user will NOT mix insert() and
        insert_fifo() - they will either use one all of the time, or the
        other all of the time.
        """
        if self.is_empty():
            self.insert(0, data)
        else:
            self.insert(self._queue[-1].get_key(), data)

    def get_min(self) -> Any:
        """
        Return the highest priority value from the queue, but do not remove it
        """
        if self.is_empty():
            return None
        return self._queue[1].get_value()

    def remove_min(self) -> Any:
        """
        Extract (remove) the highest priority value from the queue.
        You must then maintain the queue to ensure priority order.
        """
        if self.is_empty():
            return None
        min_val = self._queue[1].get_value()
        self._queue[1], self._queue[self._size] = self._queue[self._size], self._queue[1]
        self._queue.pop()
        self._size -= 1
        self._sink(1)
        return min_val

    def get_size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0
