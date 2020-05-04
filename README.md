# CS 170 Project (Spring 2020)

Local search + simulated annealing + random restarts = our solver for minimum average pairwise distance in the network routing problem.

### Contributors
Gautam Mittal, Adi Ganapathi, Amit Narang

## Installation
All code is written in Python 3. 

Create a virtual environment and install all relevant dependencies:
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Generating solutions
To run the solver on an input file:
```
python solver.py inputs/small-271.in
```

To run the solver on multiple input files:
```
python solver.py inputs/small-271.in inputs/large-123.in inputs/medium-4.in
```

To run the solver on all inputs:
```
python solve_all.py
```

These programs will generate relevant `.out` files in an `outputs` folder.

## Generating solutions (in the cloud)
Sometimes our solver takes a long time to run. Here's a way to speed things up by distributing the work across multiple machines. We used Google Compute Engine, but any set of computers with a public IP addresses should work.

Create an `ips.txt` in the root of the repository, for example:
```
35.236.119.37
34.125.109.175
34.125.249.69
34.106.218.210
34.94.119.105
34.94.190.240
34.94.29.188
34.83.98.129
34.82.184.47
34.83.208.163
34.125.232.183
34.125.1.110
```
Ensure that all of the machines associated with these IP addresses have a copy of this repository and have pull access. We also installed a Python 3 virtual environment in the root of each machine's repository to make sure that the latest dependencies were always installed.

Once all of the machines are setup, automatically start solvers on evenly divided subsets of all the inputs across all the machines:
```
python driver.py
```
Once the servers have finished running their individual jobs, you can use `scp` or another file transfer command to download the `outputs` folders from each machine.