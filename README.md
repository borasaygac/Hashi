# Hashi/Bridges Puzzle

The goal of this project is to encode the Bridges puzzle into SAT formulas. Each puzzle is based on a rectangular arrangement of islands where the number in each island tells how many bridges are connected to it. The object is to connect all islands according to the number of bridges so:
  1. There are no more than two bridges in the same direction.
  2. Bridges can only be vertical or horizontal and are not allowed to cross islands or other bridges.
  3. When completed, all bridges are interconnected enabling passage from any island to another

This project reads instances of islands, such as those in <hashi/tests>, turns them into an SAT instance in CNF format, finds a solution, and displays the results graphically. There is also a basic GUI.

## Instructions

You can start the raw solver without the GUI from a terminal with `python main.py` on a root level. By default, it will solve the first test file, you can customize the input by providing the number of the test file, i.e. `python main.py 8`. The GUI can be started with `python gui.py`. Please note that the generation of puzzles was not implemented fully, a possible recursive algorithm can be found as a comment in `gui.py`.

## Optimisation

Looking at the metrics, our default implementation already is quite speedy. However, we were able to even further cut down on execution time by excluding clauses belonging to the degree constraint that we can determine invalid even before running the solver. You can have a look at the difference between the sets of clauses for the degree constraint in `assets/bridge_sum.py` (list of clauses) and `assets/generate.py` (construction of clauses).

## Performance Metrics

We display the run times in seconds as a pair (not optimized, optimized).

- Test 1: (0.04, 0.03)
- Test 2: (0.08, 0.06)
- Test 3: (0.1, 0.07)
- Test 11: (0.22, 0.15)


