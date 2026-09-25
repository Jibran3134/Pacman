========================================================================
Artificial Intelligence (AI2002) — Assignment 01
Pacman Search Project
========================================================================
Student Name: Alishba Nasir | Muhammad Jibran
Roll Number:  (24I-3176) | 24i-3134
Course:       Artificial Intelligence (AI2002)
Semester:     5th Semester

1. ENVIRONMENT & PREREQUISITES
------------------------------------------------------------------------
- Python Version: Python 3.12+ (tested and verified on Python 3.12 / Windows)
- Libraries: Standard library only (sys, os, csv, time, collections, math)
- No external pip dependencies required.

2. VERIFIED AUTOGRADER SCORES (26 / 25 — 100% + Bonus)
------------------------------------------------------------------------
Command:
    python autograder.py

Results breakdown:
    Question q1 (DFS):                           3/3   [PASS]
    Question q2 (BFS):                           3/3   [PASS]
    Question q3 (UCS):                           3/3   [PASS]
    Question q4 (A* Search):                     3/3   [PASS]
    Question q5 (Corners Problem Representation): 3/3   [PASS]
    Question q6 (Corners Heuristic):             3/3   [PASS]
    Question q7 (Food Heuristic - Fast MST):     5/4   [PASS + BONUS]
    Question q8 (Closest Dot Search Agent):      3/3   [PASS]
    ----------------------------------------------------------
    TOTAL SCORE:                                26/25

3. RUN COMMANDS FOR ALL TASKS
------------------------------------------------------------------------
Task 1: Depth-First Search (DFS)
    python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
    python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=dfs

Task 2: Breadth-First Search (BFS)
    python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=bfs

Task 3: Uniform-Cost Search (UCS)
    python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
    python pacman.py -l mediumDenselyMaze -p SearchAgent -a fn=ucs
    python pacman.py -l stayEastSearch -p SearchAgent -a fn=ucs

Task 4: Greedy Best-First Search (GBFS)
    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
    python pacman.py -l mediumMaze -p SearchAgent -a fn=gbfs,heuristic=euclideanHeuristic

Task 5: A* Search
    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=nullHeuristic
    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

Task 6: Corners Problem (Multi-Goal Search)
    python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
    python pacman.py -l mediumCorners -p AStarCornersAgent -z .5

Task 7: Eating All Food Dots & Nearest Food Search
    python pacman.py -l trickySearch -p AStarFoodSearchAgent
    python pacman.py -l bigSearch -p ClosestDotSearchAgent

Custom Maze Experiments (24I3176Search.lay)
    python pacman.py -l 24I3176Search -p SearchAgent -a fn=dfs
    python pacman.py -l 24I3176Search -p SearchAgent -a fn=bfs
    python pacman.py -l 24I3176Search -p SearchAgent -a fn=ucs
    python pacman.py -l 24I3176Search -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
    python pacman.py -l 24I3176Search -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

(Add -q flag to any command to run with quiet graphics / fast mode)

4. CUSTOM MAZE EXPERIMENTAL RESULTS (layouts/24I3176Search.lay)
------------------------------------------------------------------------
Layout design incorporates deceptive dead-end pockets with deceptively low
Manhattan distances alongside an optimal bypass highway.

Algorithm          | Heuristic | Nodes Expanded | Path Cost | Optimality
-------------------|-----------|----------------|-----------|------------
DFS                | None      | 63             | 49        | Suboptimal (+20 steps)
BFS                | None      | 63             | 29        | Optimal
UCS                | None      | 63             | 29        | Optimal
GBFS (Manhattan)   | Manhattan | 33             | 33        | Suboptimal (+4 steps)
A* (Manhattan)     | Manhattan | 50             | 29        | Optimal (Pruned 13 nodes)

Key Finding:
- GBFS was seduced by the deceptive lower Manhattan heuristic into a suboptimal
  detour (cost 33 vs optimal 29).
- A* balanced g(n) + h(n), successfully pruning 13 nodes compared to BFS/UCS
  while finding the true optimal path of length 29.

5. AUTOMATED CSV TRACE LOGS
------------------------------------------------------------------------
Every execution automatically writes an 11-column state trace log into evidence/:
    evidence/dfs_*.csv
    evidence/bfs_*.csv
    evidence/ucs_*.csv
    evidence/gbfs_*.csv
    evidence/astar_*.csv

Mandatory Columns:
iteration, expanded_state, parent, action, generated_successors, frontier_before, frontier_after, explored, g, h, f

6. COURSE EVALUATION & 150-MARK RUBRIC MAPPING
------------------------------------------------------------------------
Note on Grading:
The autograder score of 26/25 (Section 2) serves as independent, automated
verification of algorithmic correctness and heuristic optimality on the standard
benchmark suite. The overall assignment grading follows the 150-mark rubric:

Component                                  | Weight | Implementation Status / Reference
-------------------------------------------|--------|-------------------------------------------------------
1. Depth-First Search (DFS)                | 10     | search.py: depthFirstSearch() [L65-L175]
2. Breadth-First Search (BFS)              | 10     | search.py: breadthFirstSearch() [L177-L254]
3. Uniform-Cost Search (UCS)               | 10     | search.py: uniformCostSearch() [L366-L470]
4. Greedy Best-First Search (GBFS)         | 10     | search.py: greedyBestFirstSearch() [L265-L364]
5. A* Search (A*)                          | 10     | search.py: aStarSearch() [L472-L580]
6. Admissible & Consistent Heuristics      | 10     | searchAgents.py: cornersHeuristic [L348], foodHeuristic (MST) [L441]
7. Multi-Goal Search Formulation           | 10     | searchAgents.py: CornersProblem [L263], ClosestDotSearchAgent [L515]
8. CSV State Trace Logging Engine          | 10     | search.py: per-iteration CSV export (11 mandatory columns)
9. Custom Maze Design & Experiments        | 10     | layouts/24I3176Search.lay & evidence/*24I3176Search.csv
10. Theoretical & Empirical Report         | 10     | report.pdf (Complexity, proofs, tables & plots)
11. Code Quality & Modularity              | 10     | Clean style, well-commented, zero forbidden files touched
12. Automated Grading Suite                | 20     | 26/25 on autograder (100% pass + bonus)
13. Viva & Conceptual Defense              | 20     | Prepared (optimality, graph vs tree search, proofs)
-------------------------------------------|--------|-------------------------------------------------------
TOTAL                                      | 150    | Complete coverage of all rubric deliverables

7. SUBMISSION REPOSITORY STRUCTURE
------------------------------------------------------------------------
├── search.py                 <- Search algorithms (DFS, BFS, UCS, GBFS, A*) + CSV logger
├── searchAgents.py           <- Multi-goal problems & heuristics (Corners, Food MST)
├── layouts/
│   └── 24I3176Search.lay     <- Custom maze designed for student 24I-3176
├── evidence/
│   ├── *.csv                 <- 30+ automated search execution CSV trace logs
│   └── screenshots/          <- Visual graphical solution captures
├── report.pdf                <- 6-10 page comprehensive academic report
├── README.txt                <- This file (reproduction guide & rubric mapping)
└── autograder.py             <- Verification autograder (all questions pass)
========================================================================

