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

from multiprocessing.reduction import duplicate

from pyrsistent import v
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
    # check whether the start state is the goal state
    startState = problem.getStartState()
    if problem.isGoalState(startState):
        return []
    # create empty stack
    stack = util.Stack()
    # create a set to store visited states
    visited = set()
    # push start state and path in the stack
    stack.push((startState, []))

    while True:
        # can't find the goal
        if stack.isEmpty():
            return
        # curr[0] is current state and curr[1] is current path
        curr = stack.pop()
        currState = curr[0]
        currPath = curr[1]
        visited.add(currState)
        # reach the goal
        if problem.isGoalState(currState):
            return currPath
        # explore the successors
        succ = problem.getSuccessors(currState)
        for s in succ:
            if s[0] not in visited:
                newPath = currPath + [s[1]]
                stack.push((s[0], newPath))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # check whether the start state is the goal state
    startState = problem.getStartState()
    if problem.isGoalState(startState):
        return []
    # create empty queue
    queue = util.Queue()
    # create a set to store visited states
    visited = set()
    # push start state and path in the queue
    queue.push((startState, []))

    while True:
        # can't find the goal
        if queue.isEmpty():
            return
        # curr[0] is current state and curr[1] is current path
        curr = queue.pop()
        currState = curr[0]
        currPath = curr[1]
        visited.add(currState)
        # reach the goal
        if problem.isGoalState(currState):
            return currPath
        # explore the successors
        succ = problem.getSuccessors(currState)
        for s in succ:
            # current successors is not visited and not in the queue
            if s[0] not in visited and s[0] not in (state[0] for state in queue.list):
                newPath = currPath + [s[1]]
                queue.push((s[0], newPath))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # check whether the start state is the goal state
    startState = problem.getStartState()
    if problem.isGoalState(startState):
        return []
    # create empty priority queue
    queue = util.PriorityQueue()
    # create a set to store visited states
    visited = set()
    # push start state, path and cost in the priority queue
    queue.push((startState, [], 0), 0)

    while True:
        # can't find the goal
        if queue.isEmpty():
            return
        # curr[0] is current state, curr[1] is current path, and curr[2] is current cost
        curr = queue.pop()
        currState = curr[0]
        currPath = curr[1]
        currCost = curr[2]
        # reach the goal
        if problem.isGoalState(currState):
            return currPath
        if currState not in visited:
            visited.add(currState)
            # explore the successors
            succ = problem.getSuccessors(currState)
            for s in succ:
                if s[0] not in visited:
                    # get the cost
                    totalCost = currCost + s[2]
                    newPath = currPath + [s[1]]
                    queue.push((s[0], newPath, totalCost), totalCost)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # check whether the start state is the goal state
    startState = problem.getStartState()
    if problem.isGoalState(startState):
        return []
    # create empty priority queue
    queue = util.PriorityQueue()
    # create a set to store visited states
    visited = set()
    # push start state, path and cost in the priority queue
    queue.push((startState, [], 0), 0)

    while True:
        # can't find the goal
        if queue.isEmpty():
            return
        # curr[0] is current state, curr[1] is current path, and curr[2] is current cost
        curr = queue.pop()
        currState = curr[0]
        currPath = curr[1]
        currCost = curr[2]
        # reach the goal
        if problem.isGoalState(currState):
            return currPath
        if currState not in visited:
            visited.add(currState)
            # explore the successors
            succ = problem.getSuccessors(currState)
            for s in succ:
                if s[0] not in visited:
                    # get the cost (g)
                    cost = currCost + s[2]
                    # get total cost (f = g + h)
                    totalCost = cost + heuristic(s[0], problem)
                    newPath = currPath + [s[1]]
                    queue.push((s[0], newPath, cost), totalCost)
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
