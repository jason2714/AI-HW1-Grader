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
    ## initialize dfs stack
    dfs_stack = util.Stack()
    ## some initialize and ans list need to be return
    ans = []
    temp = []
    route_to_current_pos = util.Stack()
    ## start point
    start_point = problem.getStartState()
    ## use now to run loop, keep start point
    now = start_point

    ## dfs visited array
    dfs_visited = []
    
    ## while loop check if the pos now is ans?
    while (not problem.isGoalState(now)):
        ## unlike hw0 the visited array was not a fixed length array, so some small diff exist
        ## when you already visit it, you can find it in the array
        if(now not in dfs_visited):
            ## if not visited, just visit it
            dfs_visited.append(now)
            successors = problem.getSuccessors(now)
            ## for loop visit all legal move
            for neighbor,direction,cost in successors:
                dfs_stack.push(neighbor)
                temp = ans + [direction]
                route_to_current_pos.push(temp)
        ## test if now is Goal
        now = dfs_stack.pop()
        ans = route_to_current_pos.pop()
    return ans

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    ## initialize bfs queue
    bfs_queue = util.Queue()
    ## some initialize and ans list need to return
    temp=[]
    ans = []
    route_to_current_pos = util.Queue()
    ## start point
    start_point = problem.getStartState()
    now = start_point

    ## bfs visited array
    bfs_visited = []
    

    ## while loop check if the pos now is ans?
    ## almost the same as dfs, the only difference is dfs use stack and bfs use queue
    while(not problem.isGoalState(now)):
        if(now not in bfs_visited):
            bfs_visited.append(now)
            successors = problem.getSuccessors(now)
            for neighbor,direction,cost in successors:
                bfs_queue.push(neighbor)
                temp = ans + [direction]
                route_to_current_pos.push(temp)
        ## test if now is Goal
        now = bfs_queue.pop()
        ans = route_to_current_pos.pop()
    return ans

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    ## PriorityQueue is a binary heap, so init one
    ## and actually a min heap can help us find least cost
    ucs_heap = util.PriorityQueue()
    ## some initialize and ans list need to return
    temp = []
    ans = []
    route_to_current_pos=util.PriorityQueue()
    ## start point
    start_point = problem.getStartState()
    now = start_point

    ## ucs visited array
    ucs_visited = []
    
    ## while loop until reach end point
    while(not problem.isGoalState(now)):
        if(now not in ucs_visited):
            ucs_visited.append(now)
            successors = problem.getSuccessors(now)
            for neighbor,direction,cost in successors:
                temp = ans + [direction]
                ## unlike the question in DC, I actually found out getCostAction worked
                pathCost = problem.getCostOfActions(temp)
                if(neighbor not in ucs_visited):
                    ucs_heap.push(neighbor,pathCost)
                    route_to_current_pos.push(temp,pathCost)
        ## test if now is Goal
        now = ucs_heap.pop()
        ans = route_to_current_pos.pop()    
    return ans

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    ## PriorityQueue is a binary heap, so init one
    ## and actually a min heap can help us find least cost
    aStar_heap = util.PriorityQueue()
    ## some initialize and ans list need to return
    temp=[]
    ans=[]
    route_to_current_pos=util.PriorityQueue()
    ## start point
    start_point = problem.getStartState()
    now = start_point
    ## aStar visited array
    aStar_visited = []

    ## while loop until reach end point
    while(not problem.isGoalState(now)):
        if(now not in aStar_visited):
            aStar_visited.append(now)
            successors = problem.getSuccessors(now)
            for neighbor,direction,cost in successors:
                temp = ans + [direction]
                ## unlike the question in DC, I actually found out getCostAction worked
                ## f(n) = g(n) + h(n)
                pathCost = problem.getCostOfActions(temp) + heuristic(neighbor,problem)
                if(neighbor not in aStar_visited):
                    aStar_heap.push(neighbor,pathCost)
                    route_to_current_pos.push(temp,pathCost)
        ## test if now is Goal
        now = aStar_heap.pop()
        ans = route_to_current_pos.pop()

        ## reference:Wiki
        ## reference:https://www.pythonpool.com/a-star-algorithm-python/#:~:text=A*%20Algorithm%20in%20Python%20or,a%20wide%20range%20of%20contexts.
    return ans


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
