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
    visted_path = []
    current_coordinates = problem.getStartState() # get initial position coordinates
    visted_path.append(current_coordinates) # record visited path
    states_history = util.Stack() #last-in-first-out
    coor_and_action = (current_coordinates, [])
    states_history.push(item = coor_and_action) #push = append typle
    # if states not empty and current_coordinates not goal( not goal = False, goal = True)
    while (states_history.isEmpty() is not True):
        state, actions = states_history.pop() #pop = get last tuple

        if problem.isGoalState(state) is True:
            return actions       
        elif problem.isGoalState(state) is False:
            visted_path.append(state)
            successor = problem.getSuccessors(state) # given coordinate, return possible coordinate and action
            for possible in successor: #search each possible coordinate and action
                coordinate = possible[0] #possible[0] = coordinate, possible[1] = actions, possible[2] = cost
                move = possible[1] #possible[1] = action
                if coordinate not in visted_path: # if possible coordinate never visted
                    actions_list = actions + [move]
                    states_history.push(item = (coordinate, actions_list))
                else:
                    pass
        else:
            pass

    all_actions_list = actions + [move]
    return all_actions_list

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visted_path = []
    current_coordinates = problem.getStartState() # get initial position coordinates
    visted_path.append(current_coordinates) # record visited path
    states_history = util.Queue() #first-in-first-out
    coor_and_action = (current_coordinates, [])
    states_history.push(item = coor_and_action) #push = append typle
    # if states not empty and current_coordinates not goal( not goal = False, goal = True)
    while states_history.isEmpty() is not True:
        state, actions = states_history.pop() #pop = get first tuple

        if problem.isGoalState(state) is True:
            return actions
        elif problem.isGoalState(state) is False:
            successor = problem.getSuccessors(state) # given coordinate, return possible coordinate and action
            for possible in successor: #search each possible coordinate and action
                coordinate = possible[0] #possible[0] = coordinate, possible[1] = move, possible[2] = cost
                move = possible[1]
                if coordinate not in visted_path: # if possible coordinate never visted
                    visted_path.append(coordinate)
                    actions_list = actions + [move]
                    states_history.push(item = (coordinate, actions_list))
                else:
                    pass
        else:
            pass

    all_actions_list = actions_list + [move]
    return all_actions_list

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    current_coordinates = problem.getStartState() # get initial position coordinates
    visted_path = []
    states_history = util.PriorityQueue() #heap

    # since only one in history, no matter priority number, line171 always pop this first
    # priority = heuristic(current_coordinates, problem)
    states_history.push(item = (current_coordinates, []), priority = 0)
    while states_history.isEmpty() is not True:
        state, actions = states_history.pop()
        if problem.isGoalState(state):
            return actions
        elif state not in visted_path:
            visted_path.append(state)
            successor = problem.getSuccessors(state) # given coordinate, return possible coordinate and action
            for possible in successor: #search each possible coordinate and action
                coordinate = possible[0] #possible[0] = coordinate, possible[1] = move, possible[2] = cost
                move = possible[1]
                if coordinate not in visted_path: # if possible coordinate never visted
                    actions_list = actions + [move]
                    # different between UFS and Astar is priority.
                    # UFS only calculate actions_list cost (called g_n)
                    # Astar is f_n = g_n + h_n (h_n is heuristic)
                    states_history.push(item = (coordinate, actions_list), priority = problem.getCostOfActions(actions_list))
                else:
                    pass
        else:
            pass

    actions_list = actions + [move]
    return actions_list

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    current_coordinates = problem.getStartState() # get initial position coordinates
    visted_path = []
    states_history = util.PriorityQueue() #heap

    # since only one in history, no matter priority number, line171 always pop this first
    # priority = heuristic(current_coordinates, problem)
    states_history.push(item = (current_coordinates, []), priority = 0)
    #print(states_history.heap) [(Priority = 0, count = 0, (current_coordinates = (5, 5), move = []))]
    while states_history.isEmpty() is not True:
        state, actions = states_history.pop()
        if problem.isGoalState(state):
            return actions
        elif state not in visted_path:
            visted_path.append(state)
            successor = problem.getSuccessors(state) # given coordinate, return possible coordinate and action
            for possible in successor: #search each possible coordinate and action
                coordinate = possible[0] #possible[0] = coordinate, possible[1] = move, possible[2] = cost
                move = possible[1]
                if coordinate not in visted_path: # if possible coordinate never visted
                    actions_list = actions + [move]
                    f_n = problem.getCostOfActions(actions_list) + heuristic(coordinate, problem) # f_n = g_n + h_n
                    # different between UFS and Astar is priority.
                    # UFS only calculate actions_list cost (called g_n)
                    # Astar is f_n = g_n + h_n (h_n is heuristic)                   
                    states_history.push(item = (coordinate, actions_list), priority = f_n)
                else:
                    pass
        else:
            pass

    actions_list = actions + [move]
    return actions_list


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
