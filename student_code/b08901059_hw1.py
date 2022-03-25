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
    def explore(now):
        if now in states:
            return False
        states.append(now)
        if problem.isGoalState(now):
            return True
        action = problem.getSuccessors(now)
        for i in range(len(action)):
            guide.push(action[i][1])
            if explore(action[i][0]):
                return True
            guide.pop()
        return False
    
    states = []
    guide = util.Stack()
    explore(problem.getStartState())
    return guide.list        

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"    
    start = problem.getStartState()
    record = {start:[None,None]}
    Q = util.Queue()
    Q.push(start)
    goal = None
    while not Q.isEmpty():
        now = Q.pop()
        if problem.isGoalState(now):
            goal = now
            break
        action = problem.getSuccessors(now)
        for i in range(len(action)):
            if not action[i][0] in record.keys():
                record[action[i][0]] = [now,action[i][1]]
                Q.push(action[i][0])
    guide = []
    while not record[goal][0] == None:
        guide.append(record[goal][1])
        goal = record[goal][0]
    guide.reverse()
    return guide    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    explored = {} # state: [ancestor, action]
    frontier = util.PriorityQueue()
    frontier.push([start,None,None], 0) # pack is [node, ancestor, action]
    goal = None
    while not frontier.isEmpty():
        cost, _, pack = frontier.heap[0]
        while pack[0] in explored.keys():
            frontier.pop()
            if frontier.isEmpty():
                break
            cost, _, pack = frontier.heap[0]
        if frontier.isEmpty():
            break
        frontier.pop()
        explored[pack[0]] = [pack[1], pack[2]]
        if problem.isGoalState(pack[0]):
            goal = pack[0]
            break
        move = problem.getSuccessors(pack[0])
        for i in range(len(move)):
            if not move[i][0] in explored.keys():
                frontier.update([move[i][0],pack[0],move[i][1]],cost+move[i][2])
    guide = []
    while not explored[goal][0] == None:
        guide.append(explored[goal][1])
        goal = explored[goal][0]
    guide.reverse()
    return guide

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    explored = {} # state: [ancestor, action]
    frontier = util.PriorityQueue()
    frontier.push([start,None,None], 0+heuristic(start,problem)) # pack is [node, ancestor, action]
    goal = None
    while not frontier.isEmpty():
        cost, _, pack = frontier.heap[0]
        while pack[0] in explored.keys():
            frontier.pop()
            if frontier.isEmpty():
                break
            cost, _, pack = frontier.heap[0]
        if frontier.isEmpty():
            break
        frontier.pop()
        explored[pack[0]] = [pack[1], pack[2]]
        if problem.isGoalState(pack[0]):
            goal = pack[0]
            break
        move = problem.getSuccessors(pack[0])
        for i in range(len(move)):
            if not move[i][0] in explored.keys():
                frontier.update([move[i][0],pack[0],move[i][1]], cost-heuristic(pack[0],problem)+move[i][2]+heuristic(move[i][0],problem))
    guide = []
    while not explored[goal][0] == None:
        guide.append(explored[goal][1])
        goal = explored[goal][0]
    guide.reverse()
    return guide

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
