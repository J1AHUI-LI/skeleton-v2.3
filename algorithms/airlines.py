"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.
"""

from structures.m_entry import Destination, Entry
from structures.m_extensible_list import ExtensibleList
from structures.m_graph import Graph
from structures.m_map import Map
from structures.m_pqueue import PriorityQueue


def has_cycles(graph: Graph) -> bool:
    """
    Task 3.1: Cycle detection

    @param: graph
      The general graph to process

    @returns: bool
      Whether or not the graph contains cycles
    """
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
    def is_in_extensible_list(elem, ext_list):
        i = 0
        while i < ext_list.get_size():
            if ext_list.get_at(i) == elem:
                return True
            i += 1
        return False

    def remove_from_extensible_list(elem, ext_list):
        i = 0
        while i < ext_list.get_size():
            if ext_list.get_at(i) == elem:
                ext_list.remove_at(i)
                break
            i += 1

    valid_nodes = ExtensibleList()
    i = 0
    while i < len(graph._nodes):
        valid_nodes.append(i)
        i += 1

    nodes_with_low_degree = ExtensibleList()
    while True:
        i = 0
        while i < valid_nodes.get_size():
            node = valid_nodes.get_at(i)
            neighbors = graph.get_neighbours(node)

            if neighbors and isinstance(neighbors[0], tuple):
                neighbors = [neighbour[0] for neighbour in neighbors if
                             is_in_extensible_list(neighbour[0], valid_nodes)]
            elif neighbors:
                neighbors = [neighbour.get_id() for neighbour in neighbors if
                             is_in_extensible_list(neighbour.get_id(), valid_nodes)]
            else:
                neighbors = []

            if len(neighbors) < min_degree:
                nodes_with_low_degree.append(node)
            i += 1

        if nodes_with_low_degree.get_size() == 0:
            break

        i = 0
        while i < nodes_with_low_degree.get_size():
            remove_from_extensible_list(nodes_with_low_degree.get_at(i), valid_nodes)
            i += 1

        nodes_with_low_degree.reset()

    return valid_nodes


def calculate_flight_budget(graph: Graph, origin: int, stopover_budget: int, monetary_budget: int) -> ExtensibleList:
    """
    Task 3.3: Big Bogan Budget Bonanza

    @param: graph
      The general graph to process
    @param: origin
      The origin from where the passenger wishes to fly
    @param: stopover_budget
      The maximum number of stopovers the passenger is willing to make
    @param: monetary_budget
      The maximum amount of money the passenger is willing to spend

    @returns: ExtensibleList
      The sorted list of viable destinations satisfying stopover and budget constraints.
    """
    distances = Map()
    stopovers = Map()
    node = 0
    while node < len(graph._nodes):
        distances.insert_kv(node, float('inf'))
        stopovers.insert_kv(node, float('inf'))
        node += 1
    distances.insert_kv(origin, 0)
    stopovers.insert_kv(origin, 0)

    pq = PriorityQueue()
    pq.insert(0, (0, origin, 0))  # Insert as a tuple (cost, node, stopovers)

    # Create a custom visited data structure to track visited nodes
    visited = [False] * len(graph._nodes)

    pq = PriorityQueue()
    pq.insert(0, (0, origin, 0))  # Insert as a tuple (cost, node, stopovers)

    destinations = ExtensibleList()

    while not pq.is_empty():
        current_tuple = pq.remove_min()
        current_cost, current_node, current_stopovers = current_tuple

        if visited[current_node]:
            continue
        visited[current_node] = True

        if current_node != origin:
            destinations.append(Destination(current_node, None, current_cost, current_stopovers))

        if current_cost > monetary_budget or current_stopovers > stopover_budget:
            continue

        neighbors = graph.get_neighbours(current_node)
        for neighbor, edge_cost in neighbors:
            new_monetary_cost = current_cost + edge_cost
            # Only increase the stopover count if the neighbor is not directly connected to the origin
            new_stopovers = current_stopovers if current_node == origin else current_stopovers + 1
            if (new_monetary_cost <= monetary_budget and new_monetary_cost <
                    distances[neighbor.get_id()] and new_stopovers <= stopover_budget):
                distances[neighbor.get_id()] = new_monetary_cost
                stopovers[neighbor.get_id()] = new_stopovers
                if not visited[neighbor.get_id()]:
                    pq.insert(new_monetary_cost, (new_monetary_cost, neighbor.get_id(), new_stopovers))

    destinations.sort()
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
    num_nodes = len(graph._nodes)
    distances = [float('inf')] * num_nodes
    visited = [False] * num_nodes
    distances[origin] = 0

    while True:
        # Get the node with the minimum distance value, from the set of nodes that haven't been processed yet.
        min_distance = float('inf')
        node_with_min_distance = None

        i = 0  # Counter to replace range
        while i < num_nodes:
            if not visited[i] and distances[i] < min_distance:
                min_distance = distances[i]
                node_with_min_distance = i
            i += 1  # Increment the counter

        # If no node was selected, then all nodes have been visited.
        if node_with_min_distance is None:
            break

        visited[node_with_min_distance] = True

        neighbours = graph.get_neighbours(node_with_min_distance)
        for neighbour, edge_cost in neighbours:
            alt_distance = distances[node_with_min_distance] + edge_cost
            if alt_distance < distances[neighbour.get_id()]:
                distances[neighbour.get_id()] = alt_distance

    # Return the results in the requested format.
    results = ExtensibleList()

    i = 0  # Counter to replace range
    while i < num_nodes:
        if distances[i] != float('inf'):
            results.append(Entry(i, distances[i]))
        i += 1  # Increment the counter

    return results


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
