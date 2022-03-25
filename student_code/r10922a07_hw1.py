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
    # return  [s,s,w]
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
    stack = util.Stack() # use stack to implement depthFirstSearch
    visit = []
    visit.append(problem.getStartState())
    path = []
    stack.push( (problem.getStartState(), path) ) # (node, path)
    ans_path = []
    while(True):
        cur_node, cur_path = stack.pop() # get the node and path 
        ans_path = cur_path
        visit.append(cur_node)
        if problem.isGoalState(cur_node): # check reach goal or not
            break
        # add successors to stack
        for succ in problem.getSuccessors(cur_node):
            if succ[0] not in visit: # check visit or not (avoid repeat node)
                stack.push( (succ[0],cur_path+[succ[1]]) )
    return  ans_path
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fifo = util.Queue() # use queue to implement breadthFirstSearch
    visit = []
    visit.append(problem.getStartState())
    path = []
    fifo.push( (problem.getStartState(), path) ) # (node, path)
    ans_path = []

    while(True):
        cur_node, cur_path = fifo.pop() # get the node and path 
        ans_path = cur_path
        visit.append(cur_node)
        if problem.isGoalState(cur_node): # check reach goal or not
            break
        for succ in problem.getSuccessors(cur_node): # add successors
            if succ[0] not in visit: # check visit or not (avoid repeat node)
                fifo.push( (succ[0],cur_path+[succ[1]]) )
                visit.append(succ[0])
    return  ans_path
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    p_queue = util.PriorityQueue() # use priorityqueue to implement uniformCostSearch
    visit = []
    # visit.append(problem.getStartState())
    path = []
    p_queue.push( (problem.getStartState(), path, 0), 0 ) # (node, path, cost)
    ans_path = []

    while(True):
        cur_node, cur_path, cur_value = p_queue.pop() # get the node ,path and cost
        ans_path = cur_path
        if cur_node in visit:
            continue
        visit.append(cur_node)
        if problem.isGoalState(cur_node): # check reach goal or not
            break
        for succ in problem.getSuccessors(cur_node): # add successors
            if succ[0] not in visit: # check visit or not (avoid repeat node)
                p_queue.update( (succ[0],cur_path+[succ[1]], cur_value+succ[2]), cur_value+succ[2] ) 

    return  ans_path
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
    p_queue = util.PriorityQueue() # use priorityqueue to implement uniformCostSearch
    visit = []
    # visit.append(problem.getStartState())
    path = []
    p_queue.push( (problem.getStartState(), path, 0), heuristic(problem.getStartState(), problem) ) 
    ans_path = []

    while(True):
        cur_node, cur_path, cur_value = p_queue.pop() # get the node, path, cost
        ans_path = cur_path
        
        if cur_node in visit:
            continue
        visit.append(cur_node)
        if problem.isGoalState(cur_node): # check reach goal or not
            break
        
        for succ in problem.getSuccessors(cur_node): # add successors
            if succ[0] not in visit: # check visit or not (avoid repeat node)
                p_queue.update( (succ[0],cur_path+[succ[1]], cur_value+succ[2]), cur_value+succ[2]+heuristic(succ[0], problem) )
            
    return  ans_path
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
