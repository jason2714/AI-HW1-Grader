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
    front = []
    paths = []
    front.append(problem.getStartState())
    paths.append([])
    explored = []

    while True:
        top = front.pop(-1)
        path = paths.pop(-1)

        if top in explored:
            continue
        if problem.isGoalState(top):
            return path
        
        explored.append(top)
        childs = problem.getSuccessors(top)
        childs = filter(
            lambda x: (x[0] not in explored) , childs)

        for c in childs:
            front.append(c[0])
            paths.append(path + [c[1]])
        

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    front = []
    paths = []
    front.append(problem.getStartState())
    paths.append([])
    explored = []

    while True:
        top = front.pop(-1)
        path = paths.pop(-1)

        if top in explored:
            continue
        if problem.isGoalState(top):
            return path
        
        explored.append(top)
        childs = problem.getSuccessors(top)
        childs = filter(
            lambda x: (x[0] not in explored) , childs)

        for c in childs:
            front.insert(0, c[0])
            paths.insert(0, path + [c[1]])

class Record:
    # record node, path and total cost together
    # I have to define __eq__ so that update() of PriorityQueue can work

    def __init__(self, node, path, cost):
        self.node = node
        self.path = path
        self.cost = cost

    def __eq__(self, o):
        try:
            if o.node == self.node:
                return True
            else:
                return False
        except:
            return False

    def __lt__(self, o):
        try:
            return (self.node, self.path, self.cost) < (o.node, o.path, o.cost)
        except:
            return 1
            
    def __str__(self):
        return str((self.node, self.path, self.cost))


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    front = util.PriorityQueue()
    front.push(Record(problem.getStartState(), [], 0), 0)
    explored = dict()

    while True:
        record = front.pop()
        
        if problem.isGoalState(record.node):
            return record.path
        
        explored[record.node] = 1

        childs = problem.getSuccessors(record.node)

        for c in childs:
            if c[0] not in explored:
                path_cost = record.cost + c[2]
                item = Record(c[0], record.path + [c[1]], path_cost)
                front.update(item, path_cost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    front = util.PriorityQueue()
    start = problem.getStartState()
    front.push(Record(start, [], 0), heuristic(start, problem))
    explored = dict()

    while True:
        record = front.pop()
        
        if problem.isGoalState(record.node):
            return record.path
        
        explored[record.node] = 1

        childs = problem.getSuccessors(record.node)

        for c in childs:
            if c[0] not in explored:
                path_cost = record.cost + c[2]
                item = Record(c[0], record.path + [c[1]], path_cost)
                front.update(item, path_cost + heuristic(c[0], problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
