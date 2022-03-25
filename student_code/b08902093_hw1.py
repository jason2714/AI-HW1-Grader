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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    # initializing the stack
    stack = util.Stack()
    stack.push((problem.getStartState(), '', 0))

    # initializing the necessary variables
    visited = []
    route = {}
    endgoal = (-1, -1)

    while True:
        if stack.isEmpty():
            break

        current_node = stack.pop()[0]
        visited.append(current_node)

        # terminate if in final state
        if problem.isGoalState(current_node):
            endgoal = current_node
            break

        successors = problem.getSuccessors(current_node)
        
        for s in successors:
            if s[0] not in visited:
                stack.push(s)
                # saving the path to follow from the specific node
                route[s[0]] = (current_node, s[1])

    r_path = []
    s = endgoal
    while True:
        if s not in route.keys():
            break
        r_path.append(route[s][1])
        s = route[s][0]

    # I don't get why I can't just return reversed(r_path) T_T
    path = []
    for n in reversed(r_path):
        path.append(n)

    return path

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # initializing the queue
    queue = util.Queue()
    queue.push((problem.getStartState(), '', 0))

    # initializing the necessary variables
    visited = []
    route = {}
    endgoal = (-1, -1)

    while True:
        if queue.isEmpty():
            break
        current_node = queue.pop()[0]
        visited.append(current_node)

        if problem.isGoalState(current_node):
            endgoal = current_node
            break
            
        successors = problem.getSuccessors(current_node)

        for s in successors:
            if s[0] not in visited and s[0] not in route.keys():
                queue.push(s)
                route[s[0]] = (current_node, s[1])
    r_path = []
    s = endgoal
    while True:
        if s not in route.keys():
            break
        r_path.append(route[s][1])
        s = route[s][0]

    # I don't get why I can't just return reversed(r_path) T_T
    path = []
    for n in reversed(r_path):
        path.append(n)
    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    priorityQueue = util.PriorityQueue()
    priorityQueue.push((problem.getStartState(), '', 0), 0)

    # initializing the necessary variables
    visited = []
    route = {}
    cost = {}
    endgoal = (-1, -1)

    while True:
        if priorityQueue.isEmpty():
            break
        current_node = priorityQueue.pop()
        current_cost = current_node[2]
        current_node = current_node[0]
        visited.append(current_node)

        if problem.isGoalState(current_node):
            endgoal = current_node
            break
            
        successors = problem.getSuccessors(current_node)

        for s in successors:
            if s[0] not in visited:
                s_cost = s[2] + current_cost
                if s[0] not in cost.keys():
                    priorityQueue.push((s[0], s[1], s_cost), s_cost)
                    cost[s[0]] = s_cost
                    route[s[0]] = (current_node, s[1])
                elif cost[s[0]] > s_cost:
                    priorityQueue.push((s[0], s[1], s_cost), s_cost)
                    cost[s[0]] = s_cost
                    route[s[0]] = (current_node, s[1])
    r_path = []
    s = endgoal
    while True:
        if s not in route.keys():
            break
        r_path.append(route[s][1])
        s = route[s][0]
    # I don't get why I can't just return reversed(r_path) T_T
    path = []
    for n in reversed(r_path):
        path.append(n)
    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    priorityQueue = util.PriorityQueue()
    priorityQueue.push((problem.getStartState(), '', 0), 0)

    # initializing the necessary variables
    visited = []
    route = {}
    cost = {}
    endgoal = (-1, -1)

    while True:
        if priorityQueue.isEmpty():
            break
        current_node = priorityQueue.pop()
        current_cost = current_node[2]
        current_node = current_node[0]
        visited.append(current_node)

        if problem.isGoalState(current_node):
            endgoal = current_node
            break
            
        successors = problem.getSuccessors(current_node)

        for s in successors:
            if s[0] not in visited:
                s_cost = s[2] + current_cost
                s_heuristic = heuristic(s[0], problem)
                if s[0] not in cost.keys():
                    priorityQueue.push((s[0], s[1], s_cost), s_cost + s_heuristic)
                    cost[s[0]] = s_cost
                    route[s[0]] = (current_node, s[1])
                elif cost[s[0]] > s_cost + s_heuristic:
                    priorityQueue.push((s[0], s[1], s_cost), s_cost + s_heuristic)
                    cost[s[0]] = s_cost
                    route[s[0]] = (current_node, s[1])
    r_path = []
    s = endgoal
    while True:
        if s not in route.keys():
            break
        r_path.append(route[s][1])
        s = route[s][0]
    # I don't get why I can't just return reversed(r_path) T_T
    path = []
    for n in reversed(r_path):
        path.append(n)
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
