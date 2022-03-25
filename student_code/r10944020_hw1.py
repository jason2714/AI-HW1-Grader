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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState() # (5, 5)
    print "Is the start a goal?", problem.isGoalState(problem.getStartState()) # False
    print "Start's successors:", problem.getSuccessors(problem.getStartState()) 
    # Start's successors: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
    """
    "*** YOUR CODE HERE ***"
    # Usually, we implement DFS via stack data structure
    stk = util.Stack()
    # Initialize the stack with the starting states
    stk.push((problem.getStartState(), None, [], []))
    # start traversal
    while not stk.isEmpty():
        cur_position, cur_direction, cur_paths, cur_visited = stk.pop()
        if problem.isGoalState(cur_position): return cur_paths
        cur_visited.append(cur_position)
        for (position, direction, cost) in problem.getSuccessors(cur_position):
            if not (position in cur_visited): # if the neighbor of the current state is visited, pass
                cur_paths.append(direction)
                stk.push((position, direction, cur_paths, cur_visited))
                cur_paths = cur_paths[:-1]
    return [] # util.raiseNotDefined()
    # P.S. Actually we don't need to push "direction" into stack, cuz we have add it in "paths"

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Usually, we implement BFS via queue data structure
    que = util.Queue()
    # Initialize the queue with the starting states
    """ # Another Solution
    que.push((problem.getStartState(), None, [], []))
    while not (que.isEmpty()):
        cur_position, cur_direction, cur_paths, cur_visited = que.pop()
        if problem.isGoalState(cur_position): return cur_paths
        if not (cur_position in cur_visited):
            cur_visited.append(cur_position)
            for (position, direction, cost) in problem.getSuccessors(cur_position):
                cur_paths.append(direction)
                que.push((position, direction, cur_paths, cur_visited))
                cur_paths = cur_paths[:-1]
    return []
    # P.S. Actually we don't need to push "direction" into stack, cuz we have add it in "paths"
    """ # Another Solution
    que.push((problem.getStartState(), None, [])) 
    visited = []
    while not (que.isEmpty()):
        cur_position, cur_direction, cur_paths = que.pop()
        if problem.isGoalState(cur_position): return cur_paths
        if not (cur_position in visited):
            for (position, direction, cost) in problem.getSuccessors(cur_position):
                cur_paths.append(direction)
                que.push((position, direction, cur_paths))
                cur_paths = cur_paths[:-1]
            visited.append(cur_position)
    return [] # util.raiseNotDefined()
    # P.S. Actually we don't need to push "direction" into stack, cuz we have add it in "paths"

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Usually, we implement UCS via priority queue data structure
    pq = util.PriorityQueue()
    # Initialize the priority queue with the starting states and costs
    pq.push((problem.getStartState(), []), 0)
    visited = []
    while not (pq.isEmpty()):
        cur_position, cur_paths = pq.pop()
        if problem.isGoalState(cur_position): return cur_paths
        if not (cur_position in visited):
            for (position, direction, cost) in problem.getSuccessors(cur_position):
                cur_paths.append(direction)
                cost = problem.getCostOfActions(cur_paths)
                pq.push((position, cur_paths), cost)
                cur_paths = cur_paths[:-1]
            visited.append(cur_position)
    return [] # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Usually, we implement A* via priority queue data structure
    pq = util.PriorityQueue()
    # Initialize the priority queue with the starting states and costs
    pq.push((problem.getStartState(), []), 0)
    visited = []
    while not (pq.isEmpty()):
        cur_position, cur_paths = pq.pop()
        if problem.isGoalState(cur_position): return cur_paths
        if not (cur_position in visited):
            for (position, direction, cost) in problem.getSuccessors(cur_position):
                cur_paths.append(direction)
                cost = problem.getCostOfActions(cur_paths) + heuristic(position, problem)
                pq.push((position, cur_paths), cost)
                cur_paths = cur_paths[:-1]
            visited.append(cur_position)
    return [] # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
