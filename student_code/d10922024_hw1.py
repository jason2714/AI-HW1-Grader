# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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

'''-----------  DFS begins  -----------'''


def depthFirstSearch(problem):
    """Search the deepest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # A container with a last-in-first-out (LIFO) queuing policy. (nodes, direction, cost)
    stack = util.Stack()
    parents, visited, path = {}, {}, []
    start = problem.getStartState()
    # print start
    startTuple = (start, '', 0)
    stack.push(startTuple)

    if problem.isGoalState(start):
        return path

    while(not problem.isGoalState(start) and not stack.isEmpty()):
        node = stack.pop()
        # print node
        visited[node[0]] = node[1]
        # print visited[node[0]]
        # print node[0]
        # print node[1]

        # check if new element just adding above is goal
        if problem.isGoalState(node[0]):
            node_solution = node[0]
            break

        # keep expanding the node --> getSuccessors should return a list of triples, (successor,
        # action, stepCost), where 'successor' is a successor to the current
        # state, 'action' is the action required to get there, and 'stepCost' is
        # the incremental cost of expanding to that successor.
        for i in problem.getSuccessors(node[0]):
            # format of i (successor) example: ((1,4), 'South', 1) --> (node, direction, cost)
            if i[0] not in visited.keys():
                # store successor and its parent
                parents[i[0]] = node[0]
                stack.push(i)

    # finding and storing the path
    while(node_solution in parents.keys()):
        node_solution_previous = parents[node_solution] # finding parent of the node solution
        path.insert(0, visited[node_solution]) # prepend direction to path <insert(n, item) inserts the item at the nth position in the list (0 at the beginning, 1 after the first element, etc ...)>
        node_solution = node_solution_previous

    # print path
    return path
    util.raiseNotDefined()

'''-----------  DFS ends  -----------'''

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # A container with a first-in-first-out (FIFO) queuing policy. (nodes, direction, cost)
    queue = util.Queue()
    parents, visited, path = {}, {}, []
    start = problem.getStartState()
    startTuple = (start, '', 0)
    queue.push(startTuple)

    if problem.isGoalState(start):
        return path

    while (not problem.isGoalState(start) and not queue.isEmpty()):
        node = queue.pop()
        visited[node[0]] = node[1]
        # print visited[node[0]]
        # print node[0]
        # print node[1]

        if problem.isGoalState(node[0]):
            node_solution = node[0]
            break

        # keep expanding the node --> getSuccessors should return a list of triples, (successor,
        # action, stepCost), where 'successor' is a successor to the current
        # state, 'action' is the action required to get there, and 'stepCost' is
        # the incremental cost of expanding to that successor.
        for i in problem.getSuccessors(node[0]):
            # format of i (successor) example: ((1,4), 'South', 1) --> (node, direction, cost)
            if i[0] not in visited.keys() and i[0] not in parents.keys():
                # not in parents.key() also the thing different between Depth and Breadth
                # store successor and its parent
                parents[i[0]] = node[0]
                queue.push(i)

    # finding and storing the path
    while (node_solution in parents.keys()):
        node_solution_previous = parents[node_solution] # finding parent of the node solution
        path.insert(0, visited[node_solution])  # prepend direction to path <insert(n, item) inserts the item at the nth position in the list (0 at the beginning, 1 after the first element, etc ...)>
        node_solution = node_solution_previous

    # print path
    return path
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited, parents, cost, path = {}, {}, {}, []
    queue = util.PriorityQueue()
    start = problem.getStartState()
    queue.push((start, '', 0), 0)
    cost[start] = 0

    if problem.isGoalState(start):
        return path

    while (not queue.isEmpty() and not problem.isGoalState(start)):
        node = queue.pop()
        visited[node[0]] = node[1]
        # print visited[node[0]]

        if problem.isGoalState(node[0]):
            node_solution = node[0]
            break

        # keep expanding the node --> getSuccessors should return a list of triples, (successor,
        # action, stepCost), where 'successor' is a successor to the current
        # state, 'action' is the action required to get there, and 'stepCost' is
        # the incremental cost of expanding to that successor.
        for i in problem.getSuccessors(node[0]):
            if i[0] not in visited.keys():
                priority = node[2] + i[2] # calculated new cost
                if i[0] in cost.keys():  # if cost was  calculated earlier
                    if cost[i[0]] <= priority: # if new cost is more than old cost, continue
                        continue
                queue.push((i[0], i[1], priority), priority) # push to queue  --> def push(self, item, priority):
                cost[i[0]] = priority # change cost and parent
                parents[i[0]] = node[0] # store successor and its parent

    # finding and storing the path
    while (node_solution in parents.keys()):
        node_solution_previous = parents[node_solution] # finding parent of the node solution
        path.insert(0, visited[node_solution]) # prepend direction to path <insert(n, item) inserts the item at the nth position in the list (0 at the beginning, 1 after the first element, etc ...)>
        node_solution = node_solution_previous

    # print path
    return path
    (util.raiseNotDefined())

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited, parents, cost, path = {}, {}, {}, []
    priority_queue = util.PriorityQueue()
    start = problem.getStartState()
    priority_queue.push((start, '', 0), nullHeuristic(start, problem))
    cost[start] = 0

    if problem.isGoalState(start):
        return path

    while (not priority_queue.isEmpty() and not problem.isGoalState(start)):
        node = priority_queue.pop()
        visited[node[0]] = node[1]

        if problem.isGoalState(node[0]):
            node_solution = node[0]
            break
        # keep expanding the node --> getSuccessors should return a list of triples, (successor,
        # action, stepCost), where 'successor' is a successor to the current
        # state, 'action' is the action required to get there, and 'stepCost' is
        # the incremental cost of expanding to that successor.
        for i in problem.getSuccessors(node[0]):
            if i[0] not in visited.keys():
                priority_queue_push = node[2] + i[2]
                # "***+ heuristic(i[0], problem) into priority IS THE DIFFERENT BETWEEN UCS & A* SEARCH**"
                priority = node[2] + i[2] + heuristic(i[0], problem) # calculated new cost = g(n) + h(n)
                
                if i[0] in cost.keys():  # if cost was  calculated earlier
                    if cost[i[0]] <= priority: # if new cost is more than old cost, continue
                        continue
                priority_queue.push((i[0], i[1], priority_queue_push), priority) # push to queue
                cost[i[0]] = priority # change cost and parent
                parents[i[0]] = node[0] # store successor and its parent

    # finding and storing the path
    while(node_solution in parents.keys()):
        node_solution_previous = parents[node_solution]  # finding parent of the node solution
        path.insert(0, visited[node_solution])  # prepend direction to path <insert(n, item) inserts the item at the nth position in the list (0 at the beginning, 1 after the first element, etc ...)>
        node_solution = node_solution_previous

    # print path
    return path
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
