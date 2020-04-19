"""
Generates graph inputs.

Usage: python make_inputs.py 10 0.4
"""
import argparse
import random
import sys

import networkx as nx

from parse import write_input_file


parser = argparse.ArgumentParser(description='Generate a random graph input.')
parser.add_argument('vertices', metavar='n', type=int, nargs='?',
                    help='number of vertices')
parser.add_argument('prob', metavar='p', type=float, nargs='?',
                    help='edge-existence probabiliity')


args = parser.parse_args()

def make_graph(n, p):
    """
    Creates an Erdos-Renyi random graph with n vertices and edge-existence probability p.
    """
    G = nx.Graph()

    # Add vertices
    G.add_nodes_from(range(n))

    # Add edges
    for i in range(n):
        for j in range(i, n):
            if i == j:
                continue
            if random.random() < p:
                dist = round(random.random() * 100 * 1000) / 1000
                G.add_edge(i, j, weight=dist)
    return G

def generate_input(n=10, p=0.1):
    write_input_file(make_graph(n, p), "./inputs/{}.in".format(n))

if __name__ == "__main__":
    assert args.vertices < 100 and args.prob > 0 and args.prob <= 1
    generate_input(args.vertices, args.prob)