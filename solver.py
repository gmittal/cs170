import numpy as np
import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance_fast
import sys

from viz import draw_graph

class Solver:
    def __init__(self, graph):
        self.graph = graph # G
        self.network = None # T

    def solve(self):
        raise NotImplementedError

class LocalSearchSolver(Solver):
    """
    Local search with simulated annealing.
    """
    def _start(self):
        """
        Starting state for T.
        """
        self.network = nx.minimum_spanning_tree(self.graph)
        assert is_valid_network(self.graph, self.network)
        
    def _neighbors(self):
        """
        Choose an node in G uniformly, and toggle its inclusion in T.
        """
        successor = self.network.copy()
        nodes = list(self.graph.nodes)
        idx = np.random.randint(0, len(nodes))
        node = nodes[idx] 

        successors = []

        if successor.has_node(node):
            successor.remove_node(node)
            assert not successor.has_node(node)
            successors.append(successor)
        else:
            successor.add_node(node)
            edges = list(self.graph.edges(node))
            for u, v in edges:
                s = successor.copy()
                if successor.has_node(v):
                    weight = self.graph.get_edge_data(u, v)
                    s.add_edge(u, v, **weight)
                successors.append(s)
            assert successor.has_node(node)

        return successors

    def _prob_sched(self, step, delta):
        """
        Simulated annealing schedule.
        """
        temperature = 3 / step
        return np.exp(-delta / temperature)

    def _search(self, steps):
        """
        Performs one iteration of local search and returns a possible T.
        """
        self._start()
        transitions = 0
        for i in range(steps):
            neighbors = [n for n in self._neighbors() if len(n.nodes) > 0 and is_valid_network(self.graph, n)]

            if neighbors == []:
                continue
            else:
                neighbor = min(neighbors, key=average_pairwise_distance_fast)

            # If the neighbor is invalid, ignore it.
            if neighbor.nodes and is_valid_network(self.graph, neighbor):
                f = average_pairwise_distance_fast(self.network)
                f_p = average_pairwise_distance_fast(neighbor)

                delta = f_p - f
                prob = self._prob_sched(transitions + 1, delta)

                # Transition?
                if delta < 0:
                    print(f_p)
                    transitions += 1
                    self.network = neighbor    
                elif np.random.random() <= prob:
                    print(f_p, prob)
                    transitions += 1
                    self.network = neighbor

        return self.network


    def solve(self):
        """
        Finds 'optimal' T network for graph.
        """
        STEPS = 5000
        RESTARTS = 10
        
        solutions = [self._search(STEPS).copy() for _ in range(RESTARTS)]
        self.network = min(solutions, key=average_pairwise_distance_fast)

        return self.network    

class ILPSolver(Solver):
    """
    ILP Solver.
    """
    def solve(self):
        pass

def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """
    solver = LocalSearchSolver(G)
    T = solver.solve()
    draw_graph(G)
    draw_graph(T)
    return T

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    T = solve(G)
    assert is_valid_network(G, T)
    
    print("="*30)
    print("Average pairwise distance: {}".format(average_pairwise_distance_fast(T)))
    output = path.split('/')[-1].split('.')[0]
    write_output_file(T, 'outputs/{}.out'.format(output))
