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

from os import access
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
    actions = list()# list to return actions
    visited = list()# list to store visited states
    stack = util.Stack()# each item is a tuple of (state, list of actions)

    # get the start state
    startState = problem.getStartState()
    if not problem.isGoalState(startState):
        item = (startState, []) 
        stack.push(item)

    while not stack.isEmpty():
        # get a state from the stack as a current state
        currentState = stack.pop()

        # if current state has not been visited, add to visited list
        if currentState[0] in visited:
            continue
        visited.append(currentState[0])

        # if current state is the goal state, get the actions and break the loop
        if problem.isGoalState(currentState[0]):
            actions = currentState[1]
            break

        # get successors of the current state and add them to the stack
        successors = problem.getSuccessors(currentState[0])
        for successor in successors:
            action = currentState[1]+[successor[1]]
            item = (successor[0], action)
            stack.push(item)

    return  actions
    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    actions = list()# list to return actions
    visited = list()# list to store visited states
    queue = util.Queue()# each item is a tuple of (state, list of actions)

    # get the start state
    startState = problem.getStartState()
    if not problem.isGoalState(startState):
        visited.append(startState)# add to visited list
        item = (startState, []) 
        queue.push(item)

    while not queue.isEmpty():
        # get a state from the queue as a current state
        currentState = queue.pop()

        # if current state is the goal state, get the actions and break the loop
        if problem.isGoalState(currentState[0]):
            actions = currentState[1]
            break

        # for each successor of the current state, if has not been visited, then add it to visited list
        successors = problem.getSuccessors(currentState[0])
        for successor in successors:
            if successor[0] not in visited:
                visited.append(successor[0])
                action = currentState[1]+[successor[1]]
                item = (successor[0], action)
                queue.push(item)

    return  actions

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    actions = list()# list to return actions
    visited = list()# list to store visited states
    paths = dict()# store path of each state
    costs = dict()# store cost of each state
    priorityQueue = util.PriorityQueue()

    # get the start state
    startState = problem.getStartState()
    if not problem.isGoalState(startState):
        priorityQueue.push(startState, 0)
        paths[startState] = []
        costs[startState] = 0

    while not priorityQueue.isEmpty():
        # get a state from the priority queue as a current state
        currentState = priorityQueue.pop()
        
        # if current state is the goal state, get its actions and break the loop
        if problem.isGoalState(currentState):
            actions = paths.get(currentState)
            break

        visited.append(currentState)

        # for each successor of the current state, if has not been visited, then update its path and cost
        successors = problem.getSuccessors(currentState)
        for successor in successors:
            if successor[0] not in visited:
                path = paths[currentState]+[successor[1]]
                cost = costs[currentState]+successor[2]
                priorityQueue.update(successor[0], cost)# update priority queue
                if successor[0] in costs:
                    if cost < costs[successor[0]]:# if already in dictionary and cost is smaller
                        paths[successor[0]] = path
                        costs[successor[0]] = cost
                else:
                    paths[successor[0]] = path
                    costs[successor[0]] = cost

    return  actions

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
    actions = list()# list to return actions
    visited = list()# list to store visited states
    paths = dict()# store path of each state
    costs = dict()# store cost of each state
    totals = dict()# store value of cost adding heuristic()
    priorityQueue = util.PriorityQueue()

    # get the start state
    startState = problem.getStartState()
    if not problem.isGoalState(startState):
        priorityQueue.push(startState, 0)
        paths[startState] = []
        costs[startState] = 0

    while not priorityQueue.isEmpty():
        # get a state from the priority queue as a current state
        currentState = priorityQueue.pop()
        
        # if current state is the goal state, get its actions and break the loop
        if problem.isGoalState(currentState):
            actions = paths.get(currentState)
            break

        visited.append(currentState)

        # for each successor of the current state, if has not been visited, then update its path, cost and total distance
        successors = problem.getSuccessors(currentState)
        for successor in successors:
            if successor[0] not in visited:
                path = paths[currentState]+[successor[1]]
                cost = costs[currentState]+successor[2]
                total = cost + heuristic(successor[0], problem)# use heuristic function to compute the estimated distance
                priorityQueue.update(successor[0], total)# update priority queue with total
                if successor[0] in totals:
                    if total < totals[successor[0]]:# if already in dictionary and total distance is smaller
                        paths[successor[0]] = path
                        costs[successor[0]] = cost
                        totals[successor[0]] = total
                else:
                    paths[successor[0]] = path
                    costs[successor[0]] = cost
                    totals[successor[0]] = total

    return  actions
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
