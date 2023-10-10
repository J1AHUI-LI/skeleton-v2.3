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
    visited = [False] * len(graph._nodes)  # Use a boolean list to track visited nodes
    predecessors = {origin: None}

    stack.push(origin)

    while not stack.is_empty():
        current = stack.pop()

        if not visited[current]:
            visited[current] = True
            visited_order.append(current)

            if current == goal:
                while current is not None:
                    path.append(current)
                    current = predecessors[current]

                # Manually reverse the path
                reversed_path = ExtensibleList()
                i = path.get_size() - 1
                while i >= 0:
                    reversed_path.append(path[i])
                    i -= 1
                path = reversed_path

                return (path, visited_order)

            neighbors = [neighbour.get_id() for neighbour in graph.get_neighbours(current)]
            for neighbor in neighbors:
                if not visited[neighbor]:
                    stack.push(neighbor)
                    if neighbor not in predecessors:
                        predecessors[neighbor] = current

    return (TraversalFailure.DISCONNECTED, visited_order)


def bfs_traversal(
        graph: Graph | LatticeGraph, origin: int, goal: int
) -> tuple[ExtensibleList, ExtensibleList] | tuple[TraversalFailure, ExtensibleList]:
    visited_order = ExtensibleList()
    path = ExtensibleList()
    queue = PriorityQueue()
    visited = [False] * len(graph._nodes)  # Use a boolean list to track visited nodes
    predecessors = {origin: None}

    queue.insert_fifo(origin)

    while not queue.is_empty():
        current = queue.remove_min()

        if not visited[current]:
            visited[current] = True
            visited_order.append(current)

            if current == goal:
                while current is not None:
                    path.append(current)
                    current = predecessors[current]

                # Manually reverse the path
                reversed_path = ExtensibleList()
                i = path.get_size() - 1
                while i >= 0:
                    reversed_path.append(path[i])
                    i -= 1
                path = reversed_path

                return (path, visited_order)

            neighbors = [neighbour.get_id() for neighbour in graph.get_neighbours(current)]
            for neighbor in neighbors:
                if not visited[neighbor]:
                    queue.insert_fifo(neighbor)
                    if neighbor not in predecessors:
                        predecessors[neighbor] = current

    return (TraversalFailure.DISCONNECTED, visited_order)


def is_in_extensible_list(elem, ext_list):
    for i in range(ext_list.get_size()):
        if ext_list[i] == elem:
            return True
    return False


def greedy_traversal(
    graph: LatticeGraph, origin: int, goal: int
) -> tuple[ExtensibleList, ExtensibleList] | tuple[TraversalFailure, ExtensibleList]:
    visited_order = ExtensibleList()
    path = ExtensibleList()
    queue = PriorityQueue()
    visited = ExtensibleList()
    predecessors = {origin: None}

    goal_coordinates = graph.get_node(goal).get_coordinates()

    # Insert the origin with distance 0
    queue.insert(0, origin)

    while not queue.is_empty():
        current = queue.remove_min()

        if not is_in_extensible_list(current, visited):
            visited.append(current)
            visited_order.append(current)

            if current == goal:
                while current is not None:
                    path.append(current)
                    current = predecessors[current]

                # Manually reverse the path
                reversed_path = ExtensibleList()
                i = path.get_size() - 1
                while i >= 0:
                    reversed_path.append(path[i])
                    i -= 1
                path = reversed_path

                return (path, visited_order)

            neighbors = [neighbour.get_id() for neighbour in graph.get_neighbours(current)]
            # current_coordinates = graph.get_node(current).get_coordinates()
            for neighbor in neighbors:
                if not is_in_extensible_list(neighbor, visited):
                    # Calculate the distance to the goal and use it as the priority
                    neighbor_coordinates = graph.get_node(neighbor).get_coordinates()
                    dist = (abs(neighbor_coordinates[0] - goal_coordinates[0]) +
                            abs(neighbor_coordinates[1] - goal_coordinates[1]))
                    queue.insert(dist, neighbor)
                    if neighbor not in predecessors:
                        predecessors[neighbor] = current

    return (TraversalFailure.DISCONNECTED, visited_order)


def distance(x_1: float, y_1: float, x_2: float, y_2: float) -> float:
    """
    Return the distance between a point at coordinate (x_1, y_1) and a point
    at coordinate (x_2, y_2). You may re-write this method with other
    parameters if you wish. Please comment on your choice of distance function.
    """
    return abs(x_2 - x_1) + abs(y_2 - y_1)


def max_traversal(
    graph: LatticeGraph, origin: int, goal: int
) -> tuple[ExtensibleList, ExtensibleList] | tuple[TraversalFailure, ExtensibleList]:
    # visited_order = ExtensibleList()
    # path = ExtensibleList()
    # queue = PriorityQueue()
    # visited = ExtensibleList()
    # predecessors = {origin: None}
    #
    # goal_coordinates = graph.get_node(goal).get_coordinates()
    #
    # # Insert the origin with distance 0
    # queue.insert(0, origin)
    #
    # while not queue.is_empty():
    #     current = queue.remove_min()  # We're still removing the min, but the priorities are negative distances
    #
    #     if not is_in_extensible_list(current, visited):
    #         visited.append(current)
    #         visited_order.append(current)
    #
    #         if current == goal:
    #             current_node = current
    #             while current_node is not None:
    #                 path.append(current_node)
    #                 current_node = predecessors[current_node]
    #
    #             # Manually reverse the path
    #             reversed_path = ExtensibleList()
    #             i = path.get_size() - 1
    #             while i >= 0:
    #                 reversed_path.append(path[i])
    #                 i -= 1
    #             path = reversed_path
    #
    #             return path, visited_order
    #
    #         neighbors = [neighbour.get_id() for neighbour in graph.get_neighbours(current)]
    #         # current_coordinates = graph.get_node(current).get_coordinates()
    #         for neighbor in neighbors:
    #             if not is_in_extensible_list(neighbor, visited):
    #                 # Calculate the negative distance to the goal and use it as the priority
    #                 neighbor_coordinates = graph.get_node(neighbor).get_coordinates()
    #                 dist = -(abs(neighbor_coordinates[0] - goal_coordinates[0]) +
    #                          abs(neighbor_coordinates[1] - goal_coordinates[1]))
    #                 queue.insert(dist, neighbor)
    #                 if neighbor not in predecessors:
    #                     predecessors[neighbor] = current
    #
    # return TraversalFailure.DISCONNECTED, visited_order
    pass