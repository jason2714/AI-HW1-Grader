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
    cur = (problem.getStartState(),'N',0)
    res = []
    visited = set()
    visited.add(cur[0])
    parent_dir = {cur[0]:'N'}
    s = util.Stack()
    s.push(cur)
    while True:
        cur = s.pop()
        if problem.isGoalState(cur[0]):
            break 
        for successor in problem.getSuccessors(cur[0]):
            if successor[0] not in visited:
                s.push(successor)
                parent_dir[successor[0]]=cur
                visited.add(cur[0])
    while parent_dir[cur[0]] != 'N':
        res.append(cur[1])
        cur = parent_dir[cur[0]]
    return res[::-1]
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    cur = (problem.getStartState(),'N',0)
    res = []
    visited = set()
    visited.add(cur[0])
    parent_dir = {cur[0]:'N'}
    s = util.Queue()
    s.push(cur)
    while True:
        cur = s.pop()
        visited.add(cur[0])
        if problem.isGoalState(cur[0]):
            break 
        for successor in problem.getSuccessors(cur[0]):
            if successor[0] not in visited:
                s.push(successor)
                parent_dir[successor[0]]=cur
                visited.add(successor[0])
    while parent_dir[cur[0]] != 'N':
        res.append(cur[1])
        cur = parent_dir[cur[0]]
    return res[::-1]

    util.raiseNotDefined()

def find_cost_in_frontier(pq, point):
    for p in pq.heap:
        if p[2][0] == point:
            return p[2][2]
    return 0

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    cur = (problem.getStartState(),'N',0)
    res = []
    visited = set()
    parent_dir = {cur[0]:'N'}
    s = util.PriorityQueue()
    s.push(cur, cur[2])
    while True:
        cur = s.pop()
        if problem.isGoalState(cur[0]):
            break
        visited.add(cur[0])
        for successor in problem.getSuccessors(cur[0]):
            if successor[0] not in visited:
                l_s = list(successor)
                l_s[2] = successor[2]+cur[2]
                successor = tuple(l_s)
                if successor[0] in parent_dir and find_cost_in_frontier(s,successor[0]) < successor[2]:
                    continue
                s.update(successor, successor[2])
                parent_dir[successor[0]]=cur

                
    while parent_dir[cur[0]] != 'N':
        res.append(cur[1])
        cur = parent_dir[cur[0]]
    return res[::-1]
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
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    cur = (problem.getStartState(),'N',0)
    res = []
    visited = set()
    parent_dir = {cur[0]:'N'}
    s = util.PriorityQueue()
    s.push(cur, cur[2])
    while True:
        cur = s.pop()
        if problem.isGoalState(cur[0]):
            break
        visited.add(cur[0])
        for successor in problem.getSuccessors(cur[0]):
            if successor[0] not in visited:
                l_s = list(successor)
                l_s[2] = successor[2]+cur[2]
                successor = tuple(l_s)
                if successor[0] in parent_dir and find_cost_in_frontier(s,successor[0]) < successor[2]:
                    continue
                s.update(successor, successor[2]+heuristic(successor[0],problem))
                parent_dir[successor[0]]=cur

                
    while parent_dir[cur[0]] != 'N':
        res.append(cur[1])
        cur = parent_dir[cur[0]]
    return res[::-1]
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
