# search.py
# ---------


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    import os, sys, csv

    evidence_dir = "evidence"
    os.makedirs(evidence_dir, exist_ok=True)
    maze_name = "unknown"
    if "-l" in sys.argv:
        maze_name = sys.argv[sys.argv.index("-l") + 1]
    elif hasattr(problem, "layoutName"):
        maze_name = getattr(problem, "layoutName")
    elif hasattr(problem, "__class__"):
        maze_name = problem.__class__.__name__

    csv_file_path = os.path.join(evidence_dir, f"dfs_{maze_name}.csv")

    start_state = problem.getStartState()
    frontier = util.Stack()
    frontier.push(0)
    nodes = {0: (start_state, None, None, 0)}
    next_node_id = 1
    visited = set()
    log_rows = []
    iteration = 0

    while not frontier.isEmpty():
        frontier_before = [str(nodes[nid][0]) for nid in reversed(frontier.list)]
        node_id = frontier.pop()
        state, parent_id, action, g = nodes[node_id]
        if state in visited:
            continue
        visited.add(state)
        iteration += 1

        parent_state = nodes[parent_id][0] if parent_id is not None else None

        if problem.isGoalState(state):
            log_rows.append({
                "iteration": iteration,
                "expanded_state": str(state),
                "parent": str(parent_state) if parent_state is not None else "None",
                "action": str(action) if action is not None else "None",
                "generated_successors": "[]",
                "frontier_before": str(frontier_before),
                "frontier_after": str([str(nodes[nid][0]) for nid in reversed(frontier.list)]),
                "explored": str(list(visited)),
                "g": g,
                "h": 0,
                "f": g
            })
            path = []
            current = node_id
            while current is not None:
                _, current, act, _ = nodes[current]
                if act is not None:
                    path.append(act)
            path.reverse()

            if log_rows:
                fieldnames = ["iteration", "expanded_state", "parent", "action", "generated_successors", "frontier_before", "frontier_after", "explored", "g", "h", "f"]
                with open(csv_file_path, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(log_rows)
            return path

        gen_succs = []
        for next_state, next_action, step_cost in reversed(problem.getSuccessors(state)):
            if next_state not in visited:
                nodes[next_node_id] = (next_state, node_id, next_action, g + step_cost)
                frontier.push(next_node_id)
                gen_succs.append((next_state, next_action, step_cost))
                next_node_id += 1

        frontier_after = [str(nodes[nid][0]) for nid in reversed(frontier.list)]
        log_rows.append({
            "iteration": iteration,
            "expanded_state": str(state),
            "parent": str(parent_state) if parent_state is not None else "None",
            "action": str(action) if action is not None else "None",
            "generated_successors": str(list(reversed(gen_succs))),
            "frontier_before": str(frontier_before),
            "frontier_after": str(frontier_after),
            "explored": str(list(visited)),
            "g": g,
            "h": 0,
            "f": g
        })

    if log_rows:
        fieldnames = ["iteration", "expanded_state", "parent", "action", "generated_successors", "frontier_before", "frontier_after", "explored", "g", "h", "f"]
        with open(csv_file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(log_rows)

    return []
#.........................................
def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    import os, sys, csv
    evidence_dir = "evidence"
    os.makedirs(evidence_dir, exist_ok=True)
    maze_name = "unknown"
    if "-l" in sys.argv:
        maze_name = sys.argv[sys.argv.index("-l") + 1]
    elif hasattr(problem, "layoutName"):
        maze_name = getattr(problem, "layoutName")
    elif hasattr(problem, "__class__"):
        maze_name = problem.__class__.__name__
    csv_file_path = os.path.join(evidence_dir, f"bfs_{maze_name}.csv")
    # FIFO Queue for BFS frontier
    frontier = util.Queue()
    startState = problem.getStartState()
    frontier.push((startState, [], None, None, 0))
    explored = set()
    frontier_states = {startState}
    log_rows = []
    iteration = 0
    solution_actions = []
    while not frontier.isEmpty():
        iteration += 1
        frontier_before = [item[0] for item in reversed(frontier.list)]
        currentState, actions, parent, lastAction, g = frontier.pop()
        frontier_states.discard(currentState)
        explored.add(currentState)
        if problem.isGoalState(currentState):
            log_rows.append({
                "iteration": iteration,
                "expanded_state": str(currentState),
                "parent": str(parent) if parent is not None else "None",
                "action": str(lastAction) if lastAction is not None else "None",
                "generated_successors": "[]",
                "frontier_before": str(frontier_before),
                "frontier_after": str([item[0] for item in reversed(frontier.list)]),
                "explored": str(list(explored)),
                "g": g,
                "h": 0,
                "f": g
            })
            solution_actions = actions
            break
        successors = problem.getSuccessors(currentState)
        generated_successors = []

        for successor, action, stepCost in successors:
            if successor not in explored and successor not in frontier_states:
                next_g = g + stepCost
                frontier.push((successor, actions + [action], currentState, action, next_g))
                frontier_states.add(successor)
                generated_successors.append((successor, action, stepCost))    
        frontier_after = [item[0] for item in reversed(frontier.list)]
        log_rows.append({
            "iteration": iteration,
            "expanded_state": str(currentState),
            "parent": str(parent) if parent is not None else "None",
            "action": str(lastAction) if lastAction is not None else "None",
            "generated_successors": str(generated_successors),
            "frontier_before": str(frontier_before),
            "frontier_after": str(frontier_after),
            "explored": str(list(explored)),
            "g": g,
            "h": 0,
            "f": g
        })
    fieldnames = [
        "iteration", "expanded_state", "parent", "action",
        "generated_successors", "frontier_before", "frontier_after",
        "explored", "g", "h", "f"
    ]
    with open(csv_file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log_rows)

    return solution_actions
#.........................................
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


# .........................................
def greedyBestFirstSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest heuristic value first."""
    import os, sys, csv

    # Determine CSV output path in evidence/
    evidence_dir = "evidence"
    os.makedirs(evidence_dir, exist_ok=True)
    maze_name = "unknown"
    if "-l" in sys.argv:
        maze_name = sys.argv[sys.argv.index("-l") + 1]
    elif hasattr(problem, "layoutName"):
        maze_name = getattr(problem, "layoutName")
    elif hasattr(problem, "__class__"):
        maze_name = problem.__class__.__name__
    csv_file_path = os.path.join(evidence_dir, f"gbfs_{maze_name}.csv")

    # PriorityQueue ordered strictly by heuristic value h(n)
    frontier = util.PriorityQueue()
    startState = problem.getStartState()
    start_h = heuristic(startState, problem)

    # Elements stored: (state, actions, parent, lastAction, g)
    # Priority is strictly h(n)
    frontier.push((startState, [], None, None, 0), start_h)

    explored = set()
    log_rows = []
    iteration = 0
    solution_actions = []

    while not frontier.isEmpty():
        frontier_before = [entry[2][0] for entry in frontier.heap]
        currentState, actions, parent, lastAction, g = frontier.pop()

        if currentState in explored:
            continue

        explored.add(currentState)
        curr_h = heuristic(currentState, problem)
        iteration += 1

        # Goal check
        if problem.isGoalState(currentState):
            log_rows.append({
                "iteration": iteration,
                "expanded_state": str(currentState),
                "parent": str(parent) if parent is not None else "None",
                "action": str(lastAction) if lastAction is not None else "None",
                "generated_successors": "[]",
                "frontier_before": str(frontier_before),
                "frontier_after": str([entry[2][0] for entry in frontier.heap]),
                "explored": str(list(explored)),
                "g": g,
                "h": curr_h,
                "f": curr_h
            })
            solution_actions = actions
            break

        successors = problem.getSuccessors(currentState)
        generated_successors = []

        for successor, action, stepCost in successors:
            if successor not in explored:
                h_cost = heuristic(successor, problem)
                next_g = g + stepCost
                # Priority is strictly heuristic value h(n)
                frontier.push((successor, actions + [action], currentState, action, next_g), h_cost)
                generated_successors.append((successor, action, stepCost))

        frontier_after = [entry[2][0] for entry in frontier.heap]

        log_rows.append({
            "iteration": iteration,
            "expanded_state": str(currentState),
            "parent": str(parent) if parent is not None else "None",
            "action": str(lastAction) if lastAction is not None else "None",
            "generated_successors": str(generated_successors),
            "frontier_before": str(frontier_before),
            "frontier_after": str(frontier_after),
            "explored": str(list(explored)),
            "g": g,
            "h": curr_h,
            "f": curr_h
        })

    # Write the 11 mandatory columns to evidence/
    fieldnames = [
        "iteration", "expanded_state", "parent", "action",
        "generated_successors", "frontier_before", "frontier_after",
        "explored", "g", "h", "f"
    ]
    with open(csv_file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log_rows)

    return solution_actions



def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    import os, sys, csv

    evidence_dir = "evidence"
    os.makedirs(evidence_dir, exist_ok=True)
    maze_name = "unknown"
    if "-l" in sys.argv:
        maze_name = sys.argv[sys.argv.index("-l") + 1]
    elif hasattr(problem, "layoutName"):
        maze_name = getattr(problem, "layoutName")
    elif hasattr(problem, "__class__"):
        maze_name = problem.__class__.__name__

    csv_file_path = os.path.join(evidence_dir, f"ucs_{maze_name}.csv")

    start_state = problem.getStartState()
    frontier = util.PriorityQueue()
    frontier.push(start_state, 0)
    best_cost = {start_state: 0}
    parent = {start_state: None}
    explored = set()
    log_rows = []
    iteration = 0

    while not frontier.isEmpty():
        frontier_before = [str(item[2]) for item in frontier.heap] # for logging
        state = frontier.pop()
        cost = best_cost[state]
        if state in explored:
            continue
        explored.add(state)
        iteration += 1

        parent_entry = parent[state]
        p_state = parent_entry[0] if parent_entry is not None else None
        p_action = parent_entry[1] if parent_entry is not None else None

        if problem.isGoalState(state):
            log_rows.append({
                "iteration": iteration,
                "expanded_state": str(state),
                "parent": str(p_state) if p_state is not None else "None",
                "action": str(p_action) if p_action is not None else "None",
                "generated_successors": "[]",
                "frontier_before": str(frontier_before),
                "frontier_after": str([str(item[2]) for item in frontier.heap]),
                "explored": str(list(explored)),
                "g": cost,
                "h": 0,
                "f": cost
            })
            path = []
            current = state
            while current is not None:
                parent_entry = parent[current]
                if parent_entry is None:
                    current = None
                else:
                    current, action = parent_entry
                    path.append(action)
            path.reverse()

            if log_rows:
                fieldnames = ["iteration", "expanded_state", "parent", "action", "generated_successors", "frontier_before", "frontier_after", "explored", "g", "h", "f"]
                with open(csv_file_path, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(log_rows)
            return path

        gen_succs = []
        for next_state, action, step_cost in problem.getSuccessors(state):
            next_cost = cost + step_cost
            if next_state not in best_cost or next_cost < best_cost[next_state]:
                best_cost[next_state] = next_cost
                parent[next_state] = (state, action)
                frontier.update(next_state, next_cost)
                gen_succs.append((next_state, action, step_cost))

        frontier_after = [str(item[2]) for item in frontier.heap]
        log_rows.append({
            "iteration": iteration,
            "expanded_state": str(state),
            "parent": str(p_state) if p_state is not None else "None",
            "action": str(p_action) if p_action is not None else "None",
            "generated_successors": str(gen_succs),
            "frontier_before": str(frontier_before),
            "frontier_after": str(frontier_after),
            "explored": str(list(explored)),
            "g": cost,
            "h": 0,
            "f": cost
        })

    if log_rows:
        fieldnames = ["iteration", "expanded_state", "parent", "action", "generated_successors", "frontier_before", "frontier_after", "explored", "g", "h", "f"]
        with open(csv_file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(log_rows)

    return []

# .........................................
def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    import os, sys, csv

    # Determine CSV output path in evidence/
    evidence_dir = "evidence"
    os.makedirs(evidence_dir, exist_ok=True)
    maze_name = "unknown"
    if "-l" in sys.argv:
        maze_name = sys.argv[sys.argv.index("-l") + 1]
    elif hasattr(problem, "layoutName"):
        maze_name = getattr(problem, "layoutName")
    elif hasattr(problem, "__class__"):
        maze_name = problem.__class__.__name__
    csv_file_path = os.path.join(evidence_dir, f"astar_{maze_name}.csv")

    # PriorityQueue ordered by evaluation function f(n) = g(n) + h(n)
    frontier = util.PriorityQueue()
    startState = problem.getStartState()
    start_h = heuristic(startState, problem)

    # Elements stored: (state, actions, parent, lastAction, g)
    # Priority is strictly f(n) = g(n) + h(n)
    frontier.push((startState, [], None, None, 0), start_h)

    explored = set()
    log_rows = []
    iteration = 0
    solution_actions = []

    while not frontier.isEmpty():
        frontier_before = [entry[2][0] for entry in frontier.heap]
        currentState, actions, parent, lastAction, g = frontier.pop()

        if currentState in explored:
            continue

        explored.add(currentState)
        curr_h = heuristic(currentState, problem)
        curr_f = g + curr_h
        iteration += 1

        # Goal check upon dequeue to guarantee optimal path
        if problem.isGoalState(currentState):
            log_rows.append({
                "iteration": iteration,
                "expanded_state": str(currentState),
                "parent": str(parent) if parent is not None else "None",
                "action": str(lastAction) if lastAction is not None else "None",
                "generated_successors": "[]",
                "frontier_before": str(frontier_before),
                "frontier_after": str([entry[2][0] for entry in frontier.heap]),
                "explored": str(list(explored)),
                "g": g,
                "h": curr_h,
                "f": curr_f
            })
            solution_actions = actions
            break

        successors = problem.getSuccessors(currentState)
        generated_successors = []

        for successor, action, stepCost in successors:
            if successor not in explored:
                next_g = g + stepCost
                h_cost = heuristic(successor, problem)
                f_cost = next_g + h_cost
                # Priority is strictly f(n) = g(n) + h(n)
                frontier.push((successor, actions + [action], currentState, action, next_g), f_cost)
                generated_successors.append((successor, action, stepCost))

        frontier_after = [entry[2][0] for entry in frontier.heap]

        log_rows.append({
            "iteration": iteration,
            "expanded_state": str(currentState),
            "parent": str(parent) if parent is not None else "None",
            "action": str(lastAction) if lastAction is not None else "None",
            "generated_successors": str(generated_successors),
            "frontier_before": str(frontier_before),
            "frontier_after": str(frontier_after),
            "explored": str(list(explored)),
            "g": g,
            "h": curr_h,
            "f": curr_f
        })

    # Write the 11 mandatory columns to evidence/
    fieldnames = [
        "iteration", "expanded_state", "parent", "action",
        "generated_successors", "frontier_before", "frontier_after",
        "explored", "g", "h", "f"
    ]
    with open(csv_file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log_rows)

    return solution_actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
gbfs = greedyBestFirstSearch
