# pyomo-simple-model
```
a simple pyomo optimization problem 
 Requirements: Python (pip install python)
               pyomo (pip install pyomo)
               a solver like "Gurobi", "Glpk", "Cplex"
```
```
 Files: single_node.py -> main file
        parts.py -> function for creating the optimization model
        single_node.dat -> inputs
        results.json  -> outputs
```
```
 running process:
 run in command with going to current file: pyomo solve single_node.py single_node.dat --solver=glpk
                                            or
                                            pyomo solve single_node.py single_node.dat --solver=cplex
```
