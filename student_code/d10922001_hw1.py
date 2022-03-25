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
    print "Start's successors:", problem.getSuccessors(problem.getStartState())"""
    
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    visited = set()
    path = []
    def Next_node():
        pop_info = stack.pop()
        visited.add(pop_info[0])
        neighbors = problem.getSuccessors(pop_info[0])
        return neighbors ,pop_info
    node = [problem.getStartState(), path, 1]
    stack.push(tuple(node))
    visited.add(problem.getStartState())
    current_node = problem.getStartState()
    while 1:
        if stack.isEmpty() == True or problem.isGoalState(current_node)==True:
            break
        else:
            neighbors, pop_info = Next_node()
            for i in range(0,len(neighbors)):
                if neighbors[i][0] in visited:
                    continue
                else:
                    try:
                        current_node, direction = neighbors[i][0], neighbors[i][1]
                        node = [neighbors[i][0]]
                        node.append(pop_info[1]+[neighbors[i][1]])
                    except:
                        break
                    stack.push(tuple(node))
    ans = pop_info[1]+[direction]
    return ans
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited = set()
    queue = util.Queue()
    path = []
    def Next_node(neighbors,pop_info):
        for i in range(0,len(neighbors)):
            if neighbors[i][0] in visited:
                continue
            else:
                tmp = [neighbors[i][0]]
                tmp.append(pop_info[1]+[neighbors[i][1]])
                visited.add(neighbors[i][0])
                queue.push(tuple(tmp))
    node = [problem.getStartState(), path, 1]
    visited.add(problem.getStartState())
    queue.push(tuple(node))
    while 1:
        if queue.isEmpty() == True:
            break
        try:
            pop_info = queue.pop()
            status = problem.isGoalState(pop_info[0])
        except:
            break
        if status == True:
            return pop_info[1]
        Next_node(problem.getSuccessors(pop_info[0]),pop_info)
    return pop_info[1]
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited = set()
    priority_queue = util.PriorityQueue()
    path = []
    def Next_node(neighbors,pop_info):
        for i in range(0,len(neighbors)):
            if neighbors[i][0] in visited:
                continue
            else:
                tmp = [neighbors[i][0]]
                tmp.append(pop_info[1]+[neighbors[i][1]])
                priority_queue.push(tuple(tmp), problem.getCostOfActions(pop_info[1]+[neighbors[i][1]]))
    node = [problem.getStartState(), path]
    priority_queue.push(tuple(node) ,1)
    while 1:
        if priority_queue.isEmpty()== True:
            break
        try:
            pop_info = priority_queue.pop()
            status = problem.isGoalState(pop_info[0])
        except:
            break
        if status == True:
            return pop_info[1]
        if pop_info[0] not in visited:
            Next_node(problem.getSuccessors(pop_info[0]),pop_info)
        visited.add(pop_info[0])
    return pop_info[1]
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
    visited = set()
    priority_queue = util.PriorityQueue()
    path = []
    def Next_node(neighbors, pop_info):
        for i in range(0,len(neighbors)):
            if neighbors[i][0] in visited:
                continue
            else:
                tmp = [neighbors[i][0]]
                tmp.append(pop_info[1]+[neighbors[i][1]])
                priority_queue.push(tuple(tmp), problem.getCostOfActions(pop_info[1]+[neighbors[i][1]])+heuristic(neighbors[i][0], problem))
    node = [problem.getStartState(), path]
    priority_queue.push(tuple(node), nullHeuristic(problem.getStartState(), problem))
    while 1:
        if priority_queue.isEmpty() == True:
            break
        try:
            pop_info = priority_queue.pop()
            status = problem.isGoalState(pop_info[0])
        except:
            break
        if status == True:
            return pop_info[1]
        if pop_info[0] not in visited:
            Next_node(problem.getSuccessors(pop_info[0]),pop_info)
        visited.add(pop_info[0])
    return pop_info[1]
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
