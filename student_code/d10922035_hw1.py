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
    #print('')
    #print("Start:", problem.getStartState())
    #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    #print("Start's successors:", problem.getSuccessors())
    #print('')

    stack = util.Stack() ## store all
    visited = set()  ## store coordinate
    stack.push((problem.getStartState(), [])) ## first one has no direction

    while not (stack.isEmpty()):
        coordinate, path = stack.pop()  ## curr is all
        visited.add(coordinate)

        ## first check whether current coord is the goal 
        if problem.isGoalState(coordinate):
            #print(path)
            return path

        ## if not, then we check 
        ## 1. whether there is other path
        ## 2. if not, this round the stack push nothing, and next round pop again
        for i in problem.getSuccessors(coordinate):
            if i[0] not in visited:
                new_position = i[0]
                new_path = path + [i[1]]
                stack.push((new_position, new_path))

    return "No way to get to the goal"

    """
    #util.raiseNotDefined()
    """



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    queue = util.Queue() # store all
    visited = set() # store coordinate
    queue.push((problem.getStartState(), []))

    while not (queue.isEmpty()):
        coordinate, path = queue.pop() # store all
        

        if problem.isGoalState(coordinate):
            #print(path)
            return path


        if coordinate not in visited:
            visited.add(coordinate)

            for i in problem.getSuccessors(coordinate):  ## see if any following coordinates can go
                if i[0] not in visited:  ## unlike stack, queue add several coords, if add visited when pop, likely to overlap 
                    new_path = path + [i[1]]
                    new_coordinate = i[0]
                    queue.push((new_coordinate, new_path))

    return "No way to get to the goal"



    """
    # util.raiseNotDefined()
    """


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    priqueue = util.PriorityQueue()
    visited = set() # store coordinate
    priqueue.push((problem.getStartState(), [], 0), 0)

    while not (priqueue.isEmpty()):
        coordinate, path, cost = priqueue.pop() # store all

        if problem.isGoalState(coordinate):
            #print(path)
            return path

        if coordinate not in visited:
            visited.add(coordinate)

            for i in problem.getSuccessors(coordinate):  ## see if any following coordinates can go
                #print(priqueue.heap)
                #print(problem.getSuccessors(coordinate))

                if i[0] not in visited: 
                    new_path = path + [i[1]]
                    sum_cost = cost + i[2] 
                    new_coordinate = i[0]
                    priqueue.update((new_coordinate, new_path, sum_cost), sum_cost)

    return "No way to get to the goal"

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

    priqueue = util.PriorityQueue()
    visited = set() # store coordinate
    priqueue.push((problem.getStartState(), [], 0), 0)

    while not (priqueue.isEmpty()):
        coordinate, path, cost = priqueue.pop() # store all
        
        if problem.isGoalState(coordinate):
            #print(path)
            return path

        if coordinate not in visited:
            visited.add(coordinate)

            for i in problem.getSuccessors(coordinate):  ## see if any following coordinates can go
                #print(priqueue.heap)
                #print(problem.getSuccessors(coordinate))

                if i[0] not in visited: 
                    #print(i)
                    new_path = path + [i[1]]
                    sum_cost = cost + i[2] 
                    new_coordinate = i[0]
                    f_n = sum_cost + heuristic(new_coordinate, problem)
                    priqueue.update((new_coordinate, new_path, sum_cost), f_n)

    return "No way to get to the goal"

    


    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
