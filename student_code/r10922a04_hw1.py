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
    stack = util.Stack()
    visited = util.Counter()
    # initial state and answer
    stack.push((problem.getStartState(), []))
    while not stack.isEmpty():
        c_state, c_ans = stack.pop()
        if visited[c_state] == 0:
            visited[c_state] += 1
        if problem.isGoalState(c_state):
            return c_ans
        else:
            for n_state, n_step, n_cost in problem.getSuccessors(c_state):
                if visited[n_state] == 0:
                    ans = c_ans+[n_step]
                    stack.push((n_state, ans))


def breadthFirstSearch(problem):
    queue = util.Queue()
    visited = util.Counter()
    queue.push((problem.getStartState(), []))
    while not queue.isEmpty():
        c_state, c_ans = queue.pop()
        if visited[c_state] == 0:
            visited[c_state] += 1
        if problem.isGoalState(c_state):
            return c_ans
        else:
            for n_state, n_step, n_cost in problem.getSuccessors(c_state):
                if visited[n_state] == 0:
                    ans = c_ans+[n_step]
                    queue.push((n_state, ans))
                    visited[n_state] += 1  # make sure no duplicate childrens


def uniformCostSearch(problem):
    queue = util.PriorityQueue()
    visited = util.Counter()
    queue.push((problem.getStartState(),[], 0), 0) # state ans cost priority
    while not queue.isEmpty():
        c_state, c_ans, c_cost = queue.pop() # state ans cost
        if visited[c_state] == 0: # first time visit the smallest cost, might exist other same state but cost must be bigger, the smallest one will already be returned
            visited[c_state] += 1
            if problem.isGoalState(c_state):
                return c_ans
            else:
                for n_state, n_step, n_cost in problem.getSuccessors(c_state):
                    ans = c_ans+[n_step]
                    new_cost = c_cost + n_cost
                    queue.push((n_state, ans, new_cost), new_cost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    queue = util.PriorityQueue()
    visited = util.Counter()
    queue.push((problem.getStartState(),[], 0), nullHeuristic(problem.getStartState(), problem)) # state ans cost priority
    while not queue.isEmpty():
        c_state, c_ans, c_cost = queue.pop() # state ans cost
        if visited[c_state] == 0: # first time visit the smallest cost, might exist other same state but cost must be bigger, the smallest one will already be returned
            visited[c_state] += 1
            if problem.isGoalState(c_state):
                return c_ans
            else:
                for n_state, n_step, n_cost in problem.getSuccessors(c_state):
                    ans = c_ans+[n_step]
                    new_cost = c_cost + n_cost
                    queue.push((n_state, ans, new_cost), new_cost + heuristic(n_state, problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
