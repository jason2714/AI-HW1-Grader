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
    
####################################################################################

def dfs_re(current_nodes,problem,final_path,visited_nodes):
        if problem.isGoalState(current_nodes):
            return final_path
            
        else:
            for child,direction,total_cost in problem.getSuccessors(current_nodes):
                if child not in visited_nodes:
                    final_path.append(direction)
                    visited_nodes.add(child)
                    result = dfs_re(child,problem,final_path,visited_nodes)
                    
                    if result!=None:
                        return final_path
                        
                    else:
                        final_path.pop()
            else:
                return None

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
    
    final_path = []
    visited_nodes = set()
    visited_nodes.add(problem.getStartState())
    final_path = dfs_re(problem.getStartState(),problem,final_path,visited_nodes)
    
    return final_path
    #util.raiseNotDefined()
    
####################################################################################
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    frontier_nodes = util.Queue()
    current_nodes = {"current_state": problem.getStartState(), "visited_path": [], "total_cost": 0}
    frontier_nodes.push(current_nodes)
    visited_nodes = set()
    
    while not frontier_nodes.isEmpty():
        current_nodes = frontier_nodes.pop()
        if problem.isGoalState(current_nodes["current_state"]):
            return current_nodes["visited_path"]
            
        else:
            if current_nodes["current_state"] not in visited_nodes:
                for next_node in problem.getSuccessors(current_nodes["current_state"]):
                    if next_node[0] not in visited_nodes:
                        next_node = {"current_state":next_node[0],"visited_path":current_nodes["visited_path"]+[next_node[1]],"total_cost":current_nodes["total_cost"]+next_node[2]}
                        frontier_nodes.push(next_node)
                        
                visited_nodes.add(current_nodes["current_state"])
    #util.raiseNotDefined()
    
####################################################################################
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    frontier_nodes = util.PriorityQueue()
    current_nodes = {"current_state": problem.getStartState(), "visited_path": [], "total_cost": 0}
    frontier_nodes.update(current_nodes, current_nodes["total_cost"])
    visited_nodes = set()
    
    while not frontier_nodes.isEmpty():
        current_nodes = frontier_nodes.pop()
        if problem.isGoalState(current_nodes["current_state"]):
            return current_nodes["visited_path"]
            
        else:
            if current_nodes["current_state"] not in visited_nodes:
                for next_node in problem.getSuccessors(current_nodes["current_state"]):
                    if next_node[0] not in visited_nodes:
                        next_node = {"current_state":next_node[0],"visited_path":current_nodes["visited_path"]+[next_node[1]],"total_cost":current_nodes["total_cost"]+next_node[2]}
                        frontier_nodes.update(next_node, next_node["total_cost"])
                        
                visited_nodes.add(current_nodes["current_state"])
    #util.raiseNotDefined()

####################################################################################
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    frontier_nodes = util.PriorityQueue()
    current_nodes = {"current_state": problem.getStartState(), "visited_path": [], "total_cost": 0}
    frontier_nodes.update(current_nodes, current_nodes["total_cost"]+heuristic(current_nodes["current_state"], problem))
    visited_nodes = set()
    
    while not frontier_nodes.isEmpty():
        current_nodes = frontier_nodes.pop()
        if problem.isGoalState(current_nodes["current_state"]):
            return current_nodes["visited_path"]
            
        else:
            if current_nodes["current_state"] not in visited_nodes:
                for next_node in problem.getSuccessors(current_nodes["current_state"]):
                    if next_node[0] not in visited_nodes:
                        next_node = {"current_state":next_node[0],"visited_path":current_nodes["visited_path"]+[next_node[1]],"total_cost":current_nodes["total_cost"]+next_node[2]}
                        frontier_nodes.update(next_node, next_node["total_cost"]+heuristic(next_node["current_state"], problem))
                        
                visited_nodes.add(current_nodes["current_state"])
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
