from parse import *
import networkx as nx
import os
import sys
import pandas as pd

from solver import LocalSearchSolver

if __name__ == "__main__":
    output_dir = "out"
    input_dir = "inputs"
    
    inputs = pd.read_csv('leaderboard.csv')
    # inputs = inputs.loc[inputs['rank'] > 1]
    inputs = inputs['input'].values

    for graph_name in inputs:
        G = read_input_file(f"{input_dir}/{graph_name}.in")
        solver = LocalSearchSolver(G)
        T = solver.solve()


        write_output_file(T, f"{output_dir}/{graph_name}.out")
