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
    return [s, s, w, s, w, w, s, w]


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
    pos = problem.getStartState()

    frontier = util.Stack()
    frontier.push(item=(pos, None, pos))
    parents = {}
    visited = parents.viewkeys()
    path_found = False

    while not frontier.isEmpty():
        pos, direction, parent = frontier.pop()
        parents[pos] = (direction, parent)

        if problem.isGoalState(pos):
            path_found = True
            break

        for next_pos, direction, _ in problem.getSuccessors(pos):
            if next_pos not in visited:
                frontier.push(item=(next_pos, direction, pos))

    if path_found:
        path = []
        while pos != problem.getStartState():
            direction, pos = parents[pos]  # assigns the parent of pos to pos
            path.append(direction)

        return list(reversed(path))

    raise Exception('No Path Found')


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    pos = problem.getStartState()

    frontier = util.Queue()
    frontier.push(pos)
    parents = {pos: (None, pos)}
    visited = parents.viewkeys()
    path_found = False

    while not frontier.isEmpty():
        pos = frontier.pop()

        if problem.isGoalState(pos):
            path_found = True
            break

        for next_pos, direction, _ in problem.getSuccessors(pos):
            if next_pos not in visited:
                frontier.push(next_pos)
                parents[next_pos] = (direction, pos)

    if path_found:
        path = []
        while pos != problem.getStartState():
            direction, pos = parents[pos]  # assigns the parent of pos to pos
            path.append(direction)

        return list(reversed(path))

    raise Exception('No Path Found')


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pos = problem.getStartState()

    frontier = util.PriorityQueue()
    frontier.push(item=(pos, None, 0, pos), priority=0)
    parents = {pos: (None, pos, 0)}
    visited = parents.viewkeys()
    path_found = False

    while not frontier.isEmpty():
        pos, direction, path_cost, parent = frontier.pop()

        if problem.isGoalState(pos):
            path_found = True
            break

        for next_pos, direction, cost in problem.getSuccessors(pos):
            cost += path_cost
            if next_pos not in visited or cost < parents[next_pos][2]:
                frontier.push(item=(next_pos, direction, cost, pos),
                              priority=cost)
                parents[next_pos] = (direction, pos, cost)

    if path_found:
        path = []
        while pos != problem.getStartState():
            direction, pos, _ = parents[pos]  # assigns the parent of pos to pos
            path.append(direction)

        return list(reversed(path))

    raise Exception('No Path Found')


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    pos = problem.getStartState()

    frontier = util.PriorityQueue()
    frontier.push(item=(pos, None, 0, pos), priority=0)
    parents = {pos: (None, pos, 0)}
    visited = parents.viewkeys()
    path_found = False

    while not frontier.isEmpty():
        pos, direction, path_cost, parent = frontier.pop()

        if problem.isGoalState(pos):
            path_found = True
            break

        for next_pos, direction, cost in problem.getSuccessors(pos):
            cost += path_cost
            if next_pos not in visited or cost < parents[next_pos][2]:
                frontier.push(item=(next_pos, direction, cost, pos),
                              priority=cost + heuristic(next_pos, problem))
                parents[next_pos] = (direction, pos, cost)

    if path_found:
        path = []
        while pos != problem.getStartState():
            direction, pos, _ = parents[pos]  # assigns the parent of pos to pos
            path.append(direction)

        return list(reversed(path))

    raise Exception('No Path Found')


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
