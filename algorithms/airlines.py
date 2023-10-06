"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.
"""

from structures.m_entry import Entry
from structures.m_extensible_list import ExtensibleList
from structures.m_graph import Graph
from structures.m_map import Map
from structures.m_pqueue import PriorityQueue
from structures.m_stack import Stack
from structures.m_util import Hashable, TraversalFailure


def has_cycles(graph: Graph) -> bool:
    visited = [False] * len(graph._nodes)
    predecessors = [-1] * len(graph._nodes)

    def dfs(node, parent):
        visited[node] = True
        predecessors[node] = parent

        neighbors = [neighbour.get_id() for neighbour in graph.get_neighbours(node)]
        for neighbor in neighbors:
            if not visited[neighbor]:
                if dfs(neighbor, node):
                    return True
            elif predecessors[node] != neighbor:
                return True

        return False

    for i in range(len(graph._nodes)):
        if not visited[i]:
            if dfs(i, -1):
                return True

    return False



def enumerate_hubs(graph: Graph, min_degree: int) -> ExtensibleList:
    nodes_to_remove = ExtensibleList()

    # Step 1: Calculate the degree of each node
    degrees = [len(graph.get_neighbours(node.get_id())) for node in graph._nodes]

    while True:
        nodes_to_remove.clear()

        # Step 2: Find nodes with degree less than min_degree
        for i, degree in enumerate(degrees):
            if degree < min_degree:
                nodes_to_remove.append(i)

        # If no nodes to remove, break
        if nodes_to_remove.get_size() == 0:
            break

        # Remove nodes and update degrees
        for node_id in nodes_to_remove:
            neighbors = [neighbour.get_id() for neighbour in graph.get_neighbours(node_id)]
            for neighbor in neighbors:
                degrees[neighbor] -= 1
            degrees[node_id] = 0

    hubs = ExtensibleList()
    for i, degree in enumerate(degrees):
        if degree >= min_degree:
            hubs.append(i)

    return hubs


def calculate_flight_budget(graph: Graph, origin: int, stopover_budget: int, monetary_budget: int) -> ExtensibleList:
    # Initialize distances and stopovers with infinity and -1 respectively
    distances = [float('inf')] * len(graph._nodes)
    stopovers = [-1] * len(graph._nodes)
    distances[origin] = 0
    stopovers[origin] = 0

    # Priority queue: (cost, stopovers, node_id)
    queue = PriorityQueue()
    queue.insert(0, (0, origin))

    while not queue.is_empty():
        current_cost, current_node = queue.remove_min()
        current_stopover = stopovers[current_node]

        # If we've already processed a better path to this node, skip
        if current_cost > distances[current_node]:
            continue

        for neighbour in graph.get_neighbours(current_node):
            neighbour_id = neighbour.get_id()
            edge_cost = neighbour.get_weight()

            # If we can reach the neighbour with fewer stopovers and cost, update
            if current_stopover + 1 <= stopover_budget and current_cost + edge_cost < distances[neighbour_id]:
                distances[neighbour_id] = current_cost + edge_cost
                stopovers[neighbour_id] = current_stopover + 1
                queue.insert(distances[neighbour_id], (distances[neighbour_id], neighbour_id))

    # Filter destinations based on monetary budget and sort them
    destinations = ExtensibleList()
    for i, cost in enumerate(distances):
        if cost <= monetary_budget:
            destinations.append((i, cost, stopovers[i]))

    destinations.sort(key=lambda x: (x[1], x[2], x[0]))

    return destinations


def maintenance_optimisation(graph: Graph, origin: int) -> ExtensibleList:
    """
    Task 3.4: BA Field Maintenance Optimisation

    @param: graph
      The general graph to process
    @param: origin
      The origin where the aircraft requiring maintenance is

    @returns: ExtensibleList
      The list of all reachable destinations with the shortest path costs.
      Please use the Entry type here, with the key being the node identifier,
      and the value being the cost.
    """

    # Step 1: Initialization
    num_nodes = len(graph._nodes)
    distances = [float('inf')] * num_nodes
    visited = [False] * num_nodes
    distances[origin] = 0

    queue = PriorityQueue()
    queue.insert(0, origin)  # The distance to the origin is 0

    # Step 2: Dijkstra's Algorithm
    while not queue.is_empty():
        current_distance, current_node = queue.remove_min()

        # If the node was already visited, continue
        if visited[current_node]:
            continue

        visited[current_node] = True

        for neighbour in graph.get_neighbours(current_node):
            neighbour_id = neighbour.get_id()
            edge_weight = graph.get_edge(current_node, neighbour_id).get_weight()

            # Check if the new path to the neighbour is shorter
            if distances[current_node] + edge_weight < distances[neighbour_id]:
                distances[neighbour_id] = distances[current_node] + edge_weight
                queue.insert(distances[neighbour_id], neighbour_id)

    # Step 3: Result Compilation
    result = ExtensibleList()
    for i in range(num_nodes):
        if distances[i] != float('inf') and i != origin:  # Exclude unreachable nodes and the origin
            result.append(Entry(i, distances[i]))

    # Return the result
    return result


def all_city_logistics(graph: Graph) -> Map:
    """
    Task 3.5: All City Logistics

    @param: graph
      The general graph to process

    @returns: Map
      The map containing node pairs as keys and the cost of the shortest path
      between them as values. So, the node pairs should be inserted as keys
      of the form "0_1" where 0 is the origin node and 1 is the target node
      (their type is a string using an underscore as a seperator). The
      value should be an integer (cost of the path), or a TraversalFailure
      enumeration.
    """

    pass
