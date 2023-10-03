"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.
"""

from structures.m_entry import Entry
from structures.m_extensible_list import ExtensibleList
from structures.m_graph import Graph, LatticeGraph
from structures.m_map import Map
from structures.m_pqueue import PriorityQueue
from structures.m_stack import Stack
from structures.m_util import Hashable, TraversalFailure


def dfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
) -> tuple[ExtensibleList, ExtensibleList] | tuple[TraversalFailure, ExtensibleList]:
    visited_order = ExtensibleList()
    path = ExtensibleList()
    stack = Stack()
    visited = set()

    stack.push(origin)

    while not stack.is_empty():
        current = stack.pop()

        if current not in visited:
            visited.add(current)
            visited_order.append(current)

            if current == goal:
                path.append(goal)
                return path, visited_order

            neighbors = [neighbour.get_id() for neighbour in graph.get_neighbours(current)]
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.push(neighbor)

    return (0,1)

def bfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
) -> tuple[ExtensibleList, ExtensibleList] | tuple[TraversalFailure, ExtensibleList]:
    visited_order = ExtensibleList()
    path = ExtensibleList()
    queue = PriorityQueue()
    visited = set()

    queue.insert_fifo(origin)

    while not queue.is_empty():
        current = queue.remove_min()

        if current not in visited:
            visited.add(current)
            visited_order.append(current)

            if current == goal:
                path.append(goal)
                return path, visited_order

            neighbors = graph.get_neighbours(current)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.insert_fifo(neighbor)

    return TraversalFailure.DISCONNECTED, visited_order


def greedy_traversal(
    graph: LatticeGraph, origin: int, goal: int
) -> tuple[ExtensibleList, ExtensibleList] | tuple[TraversalFailure, ExtensibleList]:
    """
    Task 2.2: Greedy Traversal

    @param: graph
      The lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[ExtensibleList, ExtensibleList]
      1. The ordered path between the origin and the goal in node IDs;
      2. The IDs of all nodes in the order they were visited.
    @returns: tuple[TraversalFailure, ExtensibleList]
      1. TraversalFailure signals that the path between the origin and the target can not be found;
      2. The IDs of all nodes in the order they were visited.
    """
    pass


def distance(x_1: float, y_1: float, x_2: float, y_2: float) -> float:
    """
    Return the distance between a point at coordinate (x_1, y_1) and a point
    at coordinate (x_2, y_2). You may re-write this method with other
    parameters if you wish. Please comment on your choice of distance function.
    """
    pass


def max_traversal(
    graph: LatticeGraph, origin: int, goal: int
) -> tuple[ExtensibleList, ExtensibleList] | tuple[TraversalFailure, ExtensibleList]:
    """
    Task 2.3: Maximize vertex visits traversal

    @param: graph
      The lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[ExtensibleList, ExtensibleList]
      1. The ordered path between the origin and the goal in node IDs;
      2. The IDs of all nodes in the order they were visited.
    @returns: tuple[TraversalFailure, ExtensibleList]
      1. TraversalFailure signals that the path between the origin and the target can not be found;
      2. The IDs of all nodes in the order they were visited.
    """
    pass
