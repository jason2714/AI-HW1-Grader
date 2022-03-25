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

from dis import disco
from functools import total_ordering
from logging import captureWarnings
import util
import copy as cp


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

def discovered(discovered, coord):
    return (coord in discovered)




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

    mouvements = []
    discovered = []


    lifo = util.Stack()
    lifo.push(([problem.getStartState()], mouvements))



    while (not lifo.isEmpty()):

        current_coord = lifo.pop()
        coord = current_coord[0][0]
        mouvements = current_coord[1]

        if  coord not in discovered:
            discovered.append(coord)
            
            if problem.isGoalState(coord):
                path = mouvements
                return path
            
            for child in problem.getSuccessors(coord):
                if not child[0] in discovered:

                    lifo.push((child, mouvements + [child[1]]))
                
    
    return path


    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    mouvements = []
    discovered = []


    fifo = util.Queue()
    fifo.push(([problem.getStartState()], mouvements))


    while (not fifo.isEmpty()):

        current_coord = fifo.pop()
        coord = current_coord[0][0]
        mouvements = current_coord[1]

        if  coord not in discovered:
            discovered.append(coord)
            
            if problem.isGoalState(coord):
                path = mouvements
                return path
            
            for child in problem.getSuccessors(coord):
                if not child[0] in discovered:
                    fifo.push((child, mouvements + [child[1]]))
                
    
    return path

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    mouvements = []
    discovered = []
    cost = 0


    pQueue = util.PriorityQueue()
    pQueue.push(([problem.getStartState()], mouvements, cost), cost)



    while (not pQueue.isEmpty()):

        current_coord = pQueue.pop()
        coord = current_coord[0][0]
        
        mouvements = current_coord[1]
        cost = current_coord[2]

        if  coord not in discovered:
            discovered.append(coord)
            
            if problem.isGoalState(coord):
                path = mouvements
                return path
            
            for child in problem.getSuccessors(coord):
                if not child[0] in discovered:
                    pQueue.update((child, mouvements + [child[1]], cost + child[2]), cost + child[2])

                
    return path
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
    
    mouvements = []
    discovered = []
    cost = 0


    pQueue = util.PriorityQueue()
    pQueue.push(([problem.getStartState()], mouvements, cost), cost)



    while (not pQueue.isEmpty()):

        current_coord = pQueue.pop()
        coord = current_coord[0][0]
        
        mouvements = current_coord[1]
        path_cost = current_coord[2]

        if  coord not in discovered:
            discovered.append(coord)
            
            if problem.isGoalState(coord):
                path = mouvements
                return path
        
            for child in problem.getSuccessors(coord):
                if not child[0] in discovered:
                    heuristic_cost = heuristic(child[0], problem)
                    mouvement_cost = child[2]
                    total_cost = mouvement_cost + path_cost
                    total_priority = heuristic_cost + mouvement_cost + path_cost
                    pQueue.update((child, mouvements + [child[1]], total_cost), total_priority)

                
    return path
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

