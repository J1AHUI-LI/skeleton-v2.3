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
      Each element of the ExtensibleList should be of type Destination - see
      m_entry.py for the definition of that type.
    """
    visited = [False] * len(graph._nodes)
    costs = [float('inf')] * len(graph._nodes)
    stopovers = [float('inf')] * len(graph._nodes)
    queue = PriorityQueue()
    destinations = ExtensibleList()

    # Initialize the origin node with 0 cost and 0 stopovers
    costs[origin] = 0
    stopovers[origin] = 0
    queue.insert(0, origin)  # The priority is the total cost

    while not queue.is_empty():
        current_cost, current = queue.remove_min()

        if not visited[current]:
            visited[current] = True

            for neighbour, weight in graph.get_neighbours(current):
                total_cost = current_cost + weight
                new_stopover = stopovers[current] + 1

                if total_cost <= monetary_budget and new_stopover <= stopover_budget:
                    if total_cost < costs[neighbour]:
                        costs[neighbour] = total_cost
                        stopovers[neighbour] = new_stopover
                        queue.insert(total_cost, neighbour)

    # Collect viable destinations
    i = 0
    while i < len(graph._nodes):  # Assuming the graph._nodes acts like a list
        if i != origin and costs[i] <= monetary_budget and stopovers[i] <= stopover_budget:
            destinations.append((i, costs[i], stopovers[i]))
        i += 1

    # Sorting the results based on stopovers and then by cost
    destinations = sorted(destinations, key=lambda x: (x[2], x[1]))

    # Create a new ExtensibleList to return the final sorted results
    result = ExtensibleList()
    for dest in destinations:
        # Assuming Destination accepts (node_id, total_cost, number_of_stopovers) as arguments
        result.append((dest[0], dest[1], dest[2]))

    return result

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
