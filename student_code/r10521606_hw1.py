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
    # LIFO queue
    states = util.Stack()
    
    action = []
    
    current = problem.getStartState()
    visited = []
    states.push((current, action))
    while not states.isEmpty() and not problem.isGoalState(current):
        current, action = states.pop()
        visited.append(current)
        for n in problem.getSuccessors(current):
            if not n[0] in visited:
                current = n[0]
                direction = n[1]
                states.push((current, action + [direction]))
                
    return action + [direction]

    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # FIFO queue
    states = util.Queue()
    
    action = []

    current = problem.getStartState()
    visited = []
    visited.append(current)

    states.push((current, action))
    while not states.isEmpty():
        current, action = states.pop()
        if problem.isGoalState(current):
            return action

        for n in problem.getSuccessors(current):
            if not n[0] in visited:
                current = n[0]
                direction = n[1]
                visited.append(current)
                states.push((current, action + [direction]))
    return action
    
    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # priority queue
    states = util.PriorityQueue()
    
    visited = []
    start = problem.getStartState()
    action = []
    cost = 0
    states.push((start, action), cost)
    while not states.isEmpty():
        state, action = states.pop()
        
        if problem.isGoalState(state):
            return action
            
        if not state in visited:
            for n in problem.getSuccessors(state):
                if not n[0] in visited:
                    current = n[0]
                    direction = n[1]
                    # since we can easily get inherit cost from .pop()
                    cost = problem.getCostOfActions(action + [direction])
                    # update can sort the heap
                    states.update((current, action + [direction]), cost)
        visited.append(state)
        
    return action

    # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"    
    # priority queue
    states = util.PriorityQueue()
    
    visited = []
    start = problem.getStartState()
    action = []
    cost = nullHeuristic(start, problem)
    states.push((start, action), cost)
    while not states.isEmpty():
        state, action = states.pop()
        
        if problem.isGoalState(state):
            return action
            
        if not state in visited:
            for n in problem.getSuccessors(state):
                if not n[0] in visited:
                    current = n[0]
                    direction = n[1]
                    # UCS + cost from heuristic
                    cost = problem.getCostOfActions(action + [direction]) + heuristic(current, problem)
                    # update can sort the heap
                    states.update((current, action + [direction]), cost)
        visited.append(state)
        
    return action
    
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
