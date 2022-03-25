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
import heapq

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
    class node:
        def __init__(self, pos, direct, cost, parent):
            self.pos = pos
            self.direct = direct
            self.cost = cost
            self.parent = parent
        def getPos(self):
            return self.pos
        def getDirect(self):
            return self.direct
        def getParent(self):
            return self.parent

    start_node = node(problem.getStartState(), None, 0, None)
    candidate_list = util.Stack()
    candidate_list.push(start_node)
    explored_list = set([])
    now_node = None
    path = []
    while not candidate_list.isEmpty():
        now_node = candidate_list.pop()
        if problem.isGoalState(now_node.getPos()):
            break
        explored_list.add(now_node.getPos())
        successors = problem.getSuccessors(now_node.getPos())
        for i in range(len(successors)):
            if successors[i][0] not in explored_list:
                successor_node = node(successors[i][0], successors[i][1], successors[i][2], now_node)
                candidate_list.push(successor_node)

    #track back
    while now_node != start_node:
        path.append(now_node.getDirect())
        now_node = now_node.getParent()
    path.reverse() 
    return path

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    class node:
        def __init__(self, pos, direct, cost, parent):
            self.pos = pos
            self.direct = direct
            self.cost = cost
            self.parent = parent
        def getPos(self):
            return self.pos
        def getDirect(self):
            return self.direct
        def getParent(self):
            return self.parent

    start_node = node(problem.getStartState(), None, 0, None)
    candidate_list = util.Queue()
    candidate_list.push(start_node)
    candidate_pos_list = set([])
    explored_list = set([])
    path = []
    now_node = None
    while not candidate_list.isEmpty():
        now_node = candidate_list.pop()
        if problem.isGoalState(now_node.getPos()):
            break
        explored_list.add(now_node.getPos())
        successors = problem.getSuccessors(now_node.getPos())
        for i in range(len(successors)):
            if successors[i][0] not in explored_list and successors[i][0] not in candidate_pos_list:
                successor_node = node(successors[i][0], successors[i][1], successors[i][2], now_node)
                candidate_list.push(successor_node)
                candidate_pos_list.add(successor_node.getPos())

    #track back
    while now_node != start_node:
        path.append(now_node.getDirect())
        now_node = now_node.getParent()
    path.reverse() 
    return path


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    class node:
        def __init__(self, pos, direct, cost, parent):
            self.pos = pos
            self.direct = direct
            self.cost = cost
            self.parent = parent
        def getPos(self):
            return self.pos
        def getDirect(self):
            return self.direct
        def getCost(self):
            return self.cost
        def getParent(self):
            return self.parent
    
    start_node = node(problem.getStartState(), None, 0, None)
    fringe_list = util.PriorityQueue()
    fringe_list.push(start_node, start_node.getCost())
    explored_list = set([])
    path = []
    now_node = None
    while not fringe_list.isEmpty():
        now_node = fringe_list.pop()
        now_cost = now_node.getCost()
        if problem.isGoalState(now_node.getPos()):
            break
        explored_list.add(now_node.getPos())
        successors = problem.getSuccessors(now_node.getPos())
        for i in range(len(successors)):
            if successors[i][0] not in explored_list:
                successor_node = node(successors[i][0], successors[i][1], successors[i][2] + now_cost, now_node)
                #modified update
                for index, (p, c, n) in enumerate(fringe_list.heap):
                    if n.getPos() == successor_node.getPos():
                        if p <= successor_node.getCost():
                            break
                        del fringe_list.heap[index]
                        fringe_list.heap.append((successor_node.getCost(), c, successor_node))
                        heapq.heapify(fringe_list.heap) 
                        break
                else:
                    fringe_list.push(successor_node, successor_node.getCost())
    #track back
    while now_node != start_node:
        path.append(now_node.getDirect())
        now_node = now_node.getParent()
    path.reverse() 
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
    class node:
        def __init__(self, pos, direct, cost, parent):
            self.pos = pos
            self.direct = direct
            self.cost = cost
            self.parent = parent
        def getPos(self):
            return self.pos
        def getDirect(self):
            return self.direct
        def getCost(self):
            return self.cost
        def getParent(self):
            return self.parent
    
    start_node = node(problem.getStartState(), None, 0 + heuristic(problem.getStartState(), problem), None)
    fringe_list = util.PriorityQueue()
    fringe_list.push(start_node, start_node.getCost())
    explored_list = set([])
    path = []
    now_node = None
    while not fringe_list.isEmpty():
        now_node = fringe_list.pop()
        now_cost = now_node.getCost()
        if problem.isGoalState(now_node.getPos()):
            break
        explored_list.add(now_node.getPos())
        successors = problem.getSuccessors(now_node.getPos())
        for i in range(len(successors)):
            if successors[i][0] not in explored_list:
                successor_node = node(successors[i][0], successors[i][1], (successors[i][2] + now_cost), now_node)
                H = heuristic(successor_node.getPos(), problem)
                #modified update
                for index, (p, c, n) in enumerate(fringe_list.heap):
                    if n.getPos() == successor_node.getPos():
                        if p <= (successor_node.getCost() + H) :
                            break
                        del fringe_list.heap[index]
                        fringe_list.heap.append(((successor_node.getCost() + H), c, successor_node))
                        heapq.heapify(fringe_list.heap) 
                        break
                else:
                    fringe_list.push(successor_node, (successor_node.getCost() + H))
    #track back
    while now_node != start_node:
        path.append(now_node.getDirect())
        now_node = now_node.getParent()
    path.reverse() 
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
