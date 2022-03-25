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
    # util.raiseNotDefined()
    map = Map()
    stack = util.Stack()
    stack.push((problem.getStartState(), None, None))           # (curPoint, prePoint, direction)

    while not stack.isEmpty():
        curPoint, prePoint, direct = stack.pop()
        if map.isPassed(curPoint):
            continue
        map.passBy(curPoint)
        stack.push((curPoint, prePoint, direct))
        if problem.isGoalState(curPoint):
            break
        for successor in problem.getSuccessors(curPoint):
            stack.push((successor[0], curPoint, successor[1]))

    path = []
    lastPrePoint = None
    while not stack.isEmpty():
        curPoint, prePoint, direct = stack.pop()
        if lastPrePoint != None and curPoint != lastPrePoint:
            continue
        lastPrePoint = prePoint
        if prePoint != None:
            path.append(direct)
    return path[::-1]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    map = Map()
    Queue = util.Queue()
    Stack = util.Stack()
    Queue.push((problem.getStartState(), None, None))           # (curPoint, prePoint, direction)

    while not Queue.isEmpty():
        curPoint, prePoint, direct = Queue.pop()
        if map.isPassed(curPoint):
            continue
        map.passBy(curPoint)
        Stack.push((curPoint, prePoint, direct))
        if problem.isGoalState(curPoint):
            break
        for successor in problem.getSuccessors(curPoint):
            Queue.push((successor[0], curPoint, successor[1]))

    path = []
    lastPrePoint = None
    while not Stack.isEmpty():
        curPoint, prePoint, direct = Stack.pop()
        if lastPrePoint != None and curPoint != lastPrePoint:
            continue
        lastPrePoint = prePoint
        if prePoint != None:
            path.append(direct)
    return path[::-1]

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    map = Map()
    PriorityQueue = util.PriorityQueue()
    Stack = util.Stack()
    PriorityQueue.push((problem.getStartState(), None, None, 0), 0)           # (curPoint, prePoint, direction, totalCost)

    while not PriorityQueue.isEmpty():
        curPoint, prePoint, direct, totalCost = PriorityQueue.pop()
        if map.isPassed(curPoint):
            continue
        map.passBy(curPoint)
        Stack.push((curPoint, prePoint, direct))
        if problem.isGoalState(curPoint):
            break
        for successor in problem.getSuccessors(curPoint):
            if map.isPassed(successor[0]):
                continue
            PriorityQueue.push((successor[0], curPoint, successor[1], totalCost + successor[2]), totalCost + successor[2])

    path = []
    lastPrePoint = None
    while not Stack.isEmpty():
        curPoint, prePoint, direct = Stack.pop()
        if lastPrePoint != None and curPoint != lastPrePoint:
            continue
        lastPrePoint = prePoint
        if prePoint != None:
            path.append(direct)
    return path[::-1]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    map = Map()
    PriorityQueue = util.PriorityQueue()
    Stack = util.Stack()

    startState = problem.getStartState()
    f = heuristic(startState, problem)                           # f(n)
    PriorityQueue.push((startState, None, None, 0), f)           # (curPoint, prePoint, direction, g(n))

    while not PriorityQueue.isEmpty():
        curPoint, prePoint, direct, g = PriorityQueue.pop()
        if map.isPassed(curPoint):
            continue
        map.passBy(curPoint)
        Stack.push((curPoint, prePoint, direct))
        if problem.isGoalState(curPoint):
            break
        for successor in problem.getSuccessors(curPoint):
            if map.isPassed(successor[0]):
                continue
            gSuccessor = g + successor[2]
            fSuccessor = gSuccessor + heuristic(successor[0], problem)
            PriorityQueue.push((successor[0], curPoint, successor[1], gSuccessor), fSuccessor)

    path = []
    lastPrePoint = None
    while not Stack.isEmpty():
        curPoint, prePoint, direct = Stack.pop()
        if lastPrePoint != None and curPoint != lastPrePoint:
            continue
        lastPrePoint = prePoint
        if prePoint != None:
            path.append(direct)
    return path[::-1]


class Map:
    def __init__(self):
        self.passed = set()

    def isPassed(self, point):
        return point in self.passed

    def passBy(self, point):
        self.passed.add(point)            


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
