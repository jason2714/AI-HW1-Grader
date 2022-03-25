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

    print "Start:", problem.getStartState() # Start: (5, 5)
    print "Is the start a goal?", problem.isGoalState(problem.getStartState()) # False
    print "Start's successors:", problem.getSuccessors(problem.getStartState()) # [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
    """

    node_parent = dict()
    direction = dict()
    stack = util.Stack()
    current = problem.getStartState()
    node_parent[current] = list()
    direction[current] = list()
    explored = [current]

    while not problem.isGoalState(current):
        for i in problem.getSuccessors(current):
            if i[0] not in node_parent:
                stack.push(i)
                node_parent[i[0]] = [current]
                direction[i[0]] = [i[1]]
            elif i[0] in node_parent:
                stack.push(i)
                node_parent[i[0]].append(current)
                direction[i[0]].append(i[1])

        if stack.isEmpty():
            return
        select = stack.pop()
        while select[0] in explored:
            select = stack.pop()
        current = select[0]
        explored.append(current)

    sol = list()
    explored.reverse()

    i = 0
    while explored[i] != problem.getStartState():
        if explored[i+1] in node_parent[explored[i]]:
            idx = node_parent[explored[i]].index(explored[i+1])
            sol.append(direction[explored[i]][idx])
            i += 1
        else:
            explored.remove(explored[i+1])

    sol.reverse()
    return sol


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    node_parent = dict()
    direction = dict()
    queue = util.Queue()
    current = problem.getStartState()
    node_parent[current] = ''

    while not problem.isGoalState(current):
        for i in problem.getSuccessors(current):
            if i[0] not in node_parent:
                queue.push(i)
                node_parent[i[0]] = current
                direction[i[0]] = i[1]

        if queue.isEmpty():
            return
        select = queue.pop()
        current = select[0]

    sol = list()

    while current != problem.getStartState():
        sol.append(direction[current])
        current = node_parent[current]

    sol.reverse()
    return sol


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    node_parent = dict()
    direction = dict()
    cost = dict()
    queue = util.PriorityQueue()
    current = problem.getStartState()
    node_parent[current] = ''
    explored = [current]
    cost[current] = 0

    while not problem.isGoalState(current):
        successors = problem.getSuccessors(current)

        for i in successors:
            if i[0] not in node_parent:
                queue.push(i, i[2] + cost[current])
                node_parent[i[0]] = current
                direction[i[0]] = i[1]
                cost[i[0]] = i[2] + cost[current]
            elif i[0] in node_parent and i[0] not in explored and i[0] != problem.getStartState:
                if i[2] + cost[current] < cost[i[0]]:
                    queue.update(i, i[2] + cost[current])
                    node_parent[i[0]] = current
                    direction[i[0]] = i[1]
                    cost[i[0]] = i[2] + cost[current]

        if queue.isEmpty():
            return
        select = queue.pop()
        explored.append(select)
        current = select[0]

    sol = list()

    while current != problem.getStartState():
        sol.append(direction[current])
        current = node_parent[current]

    sol.reverse()
    return sol


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    node_parent = dict()
    direction = dict()
    cost = dict()
    queue = util.PriorityQueue()
    current = problem.getStartState()
    node_parent[current] = ''
    explored = [current]
    cost[current] = heuristic(current, problem)

    while not problem.isGoalState(current):
        successors = problem.getSuccessors(current)

        for i in successors:
            if i[0] not in node_parent and i[0] not in explored:
                print i, i[2] + cost[current] - heuristic(current, problem) + heuristic(i[0], problem)
                queue.push(i, i[2] + cost[current] - heuristic(current, problem) + heuristic(i[0], problem))
                node_parent[i[0]] = current
                direction[i[0]] = i[1]
                cost[i[0]] = i[2] + cost[current] - heuristic(current, problem) + heuristic(i[0], problem)
            elif i[0] in node_parent and i[0] not in explored and i[0] != problem.getStartState:
                print i, i[2] + cost[current] + heuristic(i[0], problem)
                if i[2] + cost[current] - heuristic(current, problem) + heuristic(i[0], problem) < cost[i[0]]:
                    queue.update(i, i[2] + cost[current] - heuristic(current, problem) + heuristic(i[0], problem))
                    node_parent[i[0]] = current
                    direction[i[0]] = i[1]
                    cost[i[0]] = i[2] + cost[current] - heuristic(current, problem) + heuristic(i[0], problem)

        if queue.isEmpty():
            return
        select = queue.pop()
        explored.append(select)
        current = select[0]

    sol = list()

    while current != problem.getStartState():
        sol.append(direction[current])
        current = node_parent[current]

    sol.reverse()
    return sol


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
