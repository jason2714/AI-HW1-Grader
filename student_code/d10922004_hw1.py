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
    def _dFS(current_state, state_exist, find):
        if problem.isGoalState(current_state):
            return True

        successors = problem.getSuccessors(current_state)
        for next_state, action, cost in successors:
            if next_state not in state_exist and not find:
                state_exist.append(next_state)
                stk.push(action)
                find = _dFS(next_state, state_exist, find)
                if find:
                    return find
        stk.pop()
        return find

    current_state = problem.getStartState()
    state_exist = [current_state]
    stk = util.Stack() # path
    find = _dFS(current_state, state_exist, find=False)
    if find:
        return stk.list
    else:
        return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    current_state = problem.getStartState()
    state_exist = [current_state]
    q = util.Queue()
    q.push((current_state, [])) # state, shortest path to this state
    
    while not q.isEmpty():
        current_state, path = q.pop() # current state
        if problem.isGoalState(current_state):
            return path

        successors = problem.getSuccessors(current_state) # nest states
        for next_state, action, cost in successors:
            if next_state not in state_exist:
                state_exist.append(next_state)
                ext_path = path + [action]
                q.push((next_state, ext_path))
    
    if q.isEmpty():
        return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    current_state = problem.getStartState()
    state_exist = {current_state: {'path': [], 'state': [current_state], 'cost': 0},
                   'new': {'cost':9999999}} # state, shortest path to this state, state_exist, cost to this state
    pq = util.PriorityQueue()
    pq.update(current_state, 0)
    
    while not pq.isEmpty():
        current_state = pq.pop() # current state, current cost
        if problem.isGoalState(current_state):
            return state_exist[current_state]['path']

        successors = problem.getSuccessors(current_state) 
        for next_state, action, cost in successors:
            if next_state not in list(state_exist.keys()):
                state_exist[next_state] = {}
            elif state_exist[current_state]['cost'] + cost >= state_exist[next_state]['cost']:
                continue
            state_exist[next_state]['cost'] = state_exist[current_state]['cost'] + cost
            state_exist[next_state]['path'] = state_exist[current_state]['path'] + [action]
            state_exist[next_state]['state'] = state_exist[current_state]['state'] + [next_state]
            pq.update(next_state, state_exist[next_state]['cost'])
                        
    if pq.isEmpty():
        return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    current_state = problem.getStartState()
    state_exist = {current_state: {'path':[], 'state':[current_state], 'cost':0},
                   'new': {'cost':9999999}} # state, shortest path to this state, state_exist, cost to this state
    pq = util.PriorityQueue()
    pq.update(current_state, 0)
    
    while not pq.isEmpty():
        current_state = pq.pop() # current state, current cost
        if problem.isGoalState(current_state):
            return state_exist[current_state]['path']

        successors = problem.getSuccessors(current_state) 
        for next_state, action, cost in successors:
            if next_state not in list(state_exist.keys()):
                state_exist[next_state] = {}
            elif state_exist[current_state]['cost'] + cost >= state_exist[next_state]['cost']:
                continue
            state_exist[next_state]['cost'] = state_exist[current_state]['cost'] + cost
            state_exist[next_state]['path'] = state_exist[current_state]['path'] + [action]
            state_exist[next_state]['state'] = state_exist[current_state]['state'] + [next_state]
            pq.update(next_state, state_exist[next_state]['cost'] + heuristic(next_state, problem=problem))
                        
    if pq.isEmpty():
        return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
