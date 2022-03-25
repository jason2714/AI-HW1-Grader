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
    searchStack = util.Stack()
    visitedNodes = []
    currNode = problem.getStartState()
    path = []
    pathTrack = {}
    dirTo = {}
 
    searchStack.push(problem.getStartState())

    while searchStack.isEmpty() == False:
        currNode = searchStack.pop()

        if problem.isGoalState(currNode):        
            while (currNode != problem.getStartState()):
                path.append(dirTo[currNode])
                currNode = pathTrack[currNode]
            break 

        if currNode not in visitedNodes:
            visitedNodes.append(currNode)

        for succ in problem.getSuccessors(currNode):
            if not (succ[0] in visitedNodes):
                searchStack.push(succ[0])
                pathTrack[succ[0]] = currNode
                dirTo[succ[0]] = succ[1]
    path.reverse()
    print path
    return(path)
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    searchStack = util.Queue()
    visitedNodes = []
    currNode = problem.getStartState()
    path = []
    pathTrack = {}
    dirTo = {}
 
    searchStack.push(problem.getStartState())
    print problem.getStartState()
    visitedNodes.append(problem.getStartState())

    while searchStack.isEmpty() == False:
        currNode = searchStack.pop()

        if problem.isGoalState(currNode):        
            while (currNode != problem.getStartState()):
                path.append(dirTo[currNode])
                currNode = pathTrack[currNode]
            break 

        for succ in problem.getSuccessors(currNode):
            if succ[0] not in visitedNodes:
                visitedNodes.append(succ[0])
                searchStack.push(succ[0])
                pathTrack[succ[0]] = currNode
                dirTo[succ[0]] = succ[1]
    path.reverse()
    return(path)
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    searchStack = util.PriorityQueue()
    visitedNodes = []
    openNodes = []
    currNode = problem.getStartState()
    nodePrios = {}

    path = []
    pathTrack = {}
    dirTo = {}
 
    nodePrios[problem.getStartState()] = 0
    searchStack.push(problem.getStartState(), 0)
    visitedNodes.append(problem.getStartState())
    openNodes.append(problem.getStartState())

    while searchStack.isEmpty() == False:
        currNode = searchStack.pop()
        openNodes.remove(currNode)
        currNodePrio = nodePrios[currNode]

        if problem.isGoalState(currNode):        
            while (currNode != problem.getStartState()):
                path.append(dirTo[currNode])
                currNode = pathTrack[currNode]
            break

        visitedNodes.append(currNode)

        for succ in problem.getSuccessors(currNode):
            if (succ[0] not in visitedNodes) and (succ[0] not in openNodes):
                searchStack.update(succ[0],succ[2]+currNodePrio)
                pathTrack[succ[0]] = currNode
                dirTo[succ[0]] = succ[1]
                openNodes.append(succ[0])
                nodePrios[succ[0]] = succ[2]+currNodePrio

            elif (succ[0] in openNodes):
                if succ[2]+currNodePrio < nodePrios[succ[0]]:
                    dirTo[succ[0]] = succ[1]
                    pathTrack[succ[0]] = currNode
                    searchStack.update(succ[0],succ[2]+currNodePrio)
                    nodePrios[succ[0]] = succ[2]+currNodePrio

    path.reverse()
    return(path)
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
    searchStack = util.PriorityQueue()
    visitedNodes = []
    openNodes = []
    currNode = problem.getStartState()
    nodePrios = {}

    totDist = {}

    path = []
    pathTrack = {}
    dirTo = {}

    nodePrios[problem.getStartState()] = 0
    searchStack.push(problem.getStartState(), 0)
    visitedNodes.append(problem.getStartState())
    openNodes.append(problem.getStartState())
    totDist[problem.getStartState()] = 0

    while searchStack.isEmpty() == False:
        currNode = searchStack.pop()
        openNodes.remove(currNode)

        if problem.isGoalState(currNode):        
            while (currNode != problem.getStartState()):
                path.append(dirTo[currNode])
                currNode = pathTrack[currNode]
            break

        visitedNodes.append(currNode)

        for succ in problem.getSuccessors(currNode):
             
            if (succ[0] not in visitedNodes) and (succ[0] not in openNodes):
                totDist[succ[0]] = totDist[currNode] + succ[2]
                searchStack.update(succ[0], totDist[succ[0]] + heuristic(succ[0], problem))
                pathTrack[succ[0]] = currNode
                dirTo[succ[0]] = succ[1]
                openNodes.append(succ[0])
            
            elif (succ[0] in visitedNodes) and (totDist[currNode] + succ[2] < totDist[succ[0]]):

                totDist[succ[0]] = totDist[currNode] + succ[2]
                pathTrack[succ[0]] = currNode
                dirTo[succ[0]] = succ[1]
                searchStack.update(succ[0], totDist[succ[0]] + heuristic(succ[0], problem))

            elif (succ[0] in openNodes) and (totDist[currNode] + succ[2] < totDist[succ[0]]):

                totDist[succ[0]] = totDist[currNode] + succ[2]
                pathTrack[succ[0]] = currNode
                dirTo[succ[0]] = succ[1]
                searchStack.update(succ[0], totDist[succ[0]] + heuristic(succ[0], problem))
                
   
    path.reverse()
    return(path)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
