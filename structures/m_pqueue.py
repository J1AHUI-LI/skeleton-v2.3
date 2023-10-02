"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.
"""

from typing import Any

from structures.m_entry import *


class PriorityQueue:

    def __init__(self):
        self._queue = [None] * 10  # 初始化时手动分配空间
        self._size = 0  # 追踪当前队列中的元素数量

    def _resize(self):
        temp = [None] * (2 * self._size)
        for i in range(self._size):
            temp[i] = self._queue[i]
        self._queue = temp

    def insert(self, priority: int, data: Any) -> None:
        if self._size == len(self._queue):  # 如果数组已满，需要扩展数组
            self._resize()
        entry = Entry(priority, data)
        i = self._size - 1
        while i >= 0 and self._queue[i].get_key() > priority:
            i -= 1
        for j in range(self._size, i + 1, -1):
            self._queue[j] = self._queue[j - 1]
        self._queue[i + 1] = entry
        self._size += 1

    def insert_fifo(self, data: Any) -> None:
        if not self._size:
            self.insert(0, data)
        else:
            self.insert(self._queue[self._size - 1].get_key(), data)

    def get_min(self) -> Any:
        if not self.is_empty():
            return self._queue[0].get_value()
        else:
            return None

    def remove_min(self) -> Any:
        if not self.is_empty():
            min_value = self._queue[0].get_value()
            for i in range(self._size - 1):
                self._queue[i] = self._queue[i + 1]
            self._queue[self._size - 1] = None
            self._size -= 1
            return min_value
        else:
            return None

    def get_size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

if __name__ == '__main__':
    import random

    input_list = list(range(1, 100001))  # Create a list of integers from 1 to 100000
    random.shuffle(input_list)  # Shuffle the list
    pq = PriorityQueue()
    for num in input_list:
        pq.insert(num, num)  # Here, we are using the integers themselves as both the data and the priority
    output_list = []
    while not pq.is_empty():
        output_list.append(pq.remove_min())
    if output_list == sorted(output_list):
        print("Test passed: The output list is sorted.")
    else:
        print("Test failed: The output list is not sorted. Investigate the issue.")




# class PriorityQueue:
#     """
#     An implementation of the PriorityQueue ADT.
#     The provided methods consume keys and values. Keys are called "priorities"
#     and should be integers in the range [0, n] with 0 being the highest priority.
#     Values are called "data" and store the payload data of interest.
#     For convenience, you may wish to also implement the functionality provided in
#     terms of the Entry type, but this is up to you.
#     """
#
#     def __init__(self):
#         """
#         Construct the priority queue.
#         You are free to make any changes you find suitable in this function to initialise your pq.
#         """
#         self.queue = [None]  # Initialize the list with a placeholder at index 0
#         self._size = 0  # Initialize the size of the queue to 0
#
#     # Warning: This insert() signature changed as of skeleton 1.1, previously
#     # the priority and data arguments were switched
#     def insert(self, priority: int, data: Any) -> None:
#         """
#         Insert some data to the queue with a given priority.
#         Hint: FIFO queue can just always have the same priority value, no
#         need to implement an extra function.
#         """
#         if self.queue[0] is None:  # If the heap is empty, initialize it
#             self.queue[0] = (priority, data)
#             self._size += 1
#             return
#
#         self.queue.append((priority, data))  # Append the new element to the end of the list
#         self._size += 1  # Increase the size of the queue after inserting an element
#         self._bubble_up(self._size)  # Restore the heap property by bubbling up the last element
#
#     def _bubble_up(self, index: int) -> None:
#         while index // 2 > 0:  # While the element has a parent
#             parent_index = index // 2
#             if self.queue[index][0] < self.queue[parent_index][0]:  # If the child has a smaller key than the parent
#                 self.queue[index], self.queue[parent_index] = self.queue[parent_index], self.queue[index]  # Swap them
#             index = parent_index  # Move up the tree
#
#     def insert_fifo(self, data: Any) -> None:
#         """
#         UPDATE in Skeleton v2.2: Allows a user to add data for FIFO queue
#         operations. You may assume a user will NOT mix insert() and
#         insert_fifo() - they will either use one all of the time, or the
#         other all of the time.
#         """
#         self.insert(0, data)
#
#     def get_min(self) -> Any:
#         """
#         Return the highest priority value from the queue, but do not remove it
#         """
#         if self.is_empty():
#             return None
#         return self.queue[1][1]  # Return the data of the item with the highest priority without removing it
#
#     def remove_min(self) -> Any:
#         """
#         Extract (remove) the highest priority value from the queue.
#         You must then maintain the queue to ensure priority order.
#         """
#         if self.is_empty():
#             return None
#         min_val = self.queue[1][1]  # The root of the heap has the minimum key
#         self.queue[1] = self.queue[-1]  # Replace the root with the last element in the list
#         self.queue.pop()  # Remove the last element from the list
#         self._size -= 1
#         if not self.is_empty():
#             self._bubble_down(1)  # Restore the heap property by bubbling down the new root
#         return min_val
#
#     def _bubble_down(self, index: int) -> None:
#         while index * 2 < len(self.queue):  # While the element has at least one child
#             min_child_index = self._min_child(index)
#             if self.queue[index][0] > self.queue[min_child_index][0]:  # If the child has a smaller key than the parent
#                 self.queue[index], self.queue[min_child_index] = self.queue[min_child_index], self.queue[
#                     index]  # Swap them
#             index = min_child_index  # Move down the tree
#
#     def _min_child(self, index: int) -> int:
#         if index * 2 + 1 >= len(self.queue):  # If the element has only one child
#             return index * 2
#         if self.queue[index * 2][0] < self.queue[index * 2 + 1][
#             0]:  # Return the index of the child with the smaller key
#             return index * 2
#         return index * 2 + 1
#
#     def get_size(self) -> int:
#         return self._size
#
#     def is_empty(self) -> bool:
#         return self._size == 0


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
