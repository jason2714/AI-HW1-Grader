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
    

    trace = util.Stack()
    record = util.Stack()
    direction = util.Stack()
    count = 0
    
    state = problem.getStartState()
    direction.push('Start')
    trace.push(state)

   
    while problem.isGoalState(state) != True:
        flashback = 1 
        states = problem.getSuccessors(state)

        for i in states:
            if i[0] not in trace.list:
                flashback = 0
                i = list(i)
                i.append(count)
                record.push(i)
                
                
        whole_state = record.pop()
        state = whole_state[0]
        
        if flashback == 0:
            count += 1       
        elif flashback == 1:
            count = whole_state[3]+1
            trace.list = trace.list[:count]
            direction.list = direction.list[:count]

        trace.push(whole_state[0])
        direction.push(whole_state[1])     
            
    return  direction.list[1:]
    


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    node_travelled = {}
    record = util.Queue()
    direction = []
    
    state = problem.getStartState()
    initial_state = state
    node_travelled[state] = (state, 'Start')
    
    while problem.isGoalState(state) != True:
        states = problem.getSuccessors(state)
        for i in states:
            if i[0] not in node_travelled.keys():
                record.push(i)
                node_travelled[i[0]] = ((state, i[1]))                 
        state = record.pop()[0]

    while state != initial_state:
        direction.append(node_travelled[state][1])
        state = node_travelled[state][0]

    direction.reverse()
   
    return  direction
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    ## similar to dijsktra algorithm
    priority = util.PriorityQueue() ## record nodes' priority
    node_record = {} ## record nodes' ancestor
    node_travelled = [] ## node has been visited
    direction = []
    
    state = problem.getStartState()
    initial_state = state
    node_record[state] = (state, 'Start', 0)
    priority.push(state, 0)
    
    while problem.isGoalState(state) != True: 
        states = problem.getSuccessors(state)
        for i in states:
            if i[0] not in node_record.keys(): ## create the node that may be visited in the future
                node_record[i[0]] = (state, i[1], i[2]) ## {(5, 4): ((5, 5), 'South', 1)}
                priority.push(i[0], priority.heap[0][0] + i[2]) ## [(1 cost, 1 index?, (5, 4) state)]
            if i[0] in node_record.keys(): ## update the priority if needed
                if i[0] not in node_travelled: ## but not to go to the node that has been visited
                    priority.update(i[0], priority.heap[0][0] + i[2])
                    if node_record[i[0]][2] > priority.heap[0][0] + i[2]:
                        node_record[i[0]] = (state, i[1], i[2])

        pop_state = priority.pop()
        node_travelled.append(pop_state)
        state = priority.heap[0][2]

    while state != initial_state:
        direction.append(node_record[state][1])
        state = node_record[state][0]

    direction.reverse()
    return direction

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    priority = util.PriorityQueue() ## record nodes' priority
    node_record = {} ## record nodes' ancestor
    node_travelled = [] ## node has been visited
    direction = []
    
    state = problem.getStartState()
    initial_state = state
    node_record[state] = (state, 'Start', 0, heuristic(state, problem))
    priority.push(state, 0) ##avoid appending manhattaon distance at first in order to prevent not starting at the start point


        
    while problem.isGoalState(state) != True: 
        states = problem.getSuccessors(state)
        for i in states:
            if i[0] not in node_record.keys(): ## create the node that may be visited in the future
                node_record[i[0]] = (state, i[1], node_record[state][2] + i[2], heuristic(i[0], problem)) ## {(5, 4): ((5, 5), 'South', g(n), h(n))}
                priority.push(i[0], node_record[state][2] + i[2] + heuristic(i[0], problem)) ## [(1 cost, 1 index?, (5, 4) state)]
            if i[0] in node_record.keys(): ## update the priority if needed
                if i[0] not in node_travelled: ## but not to go to the node that has been visited
                    priority.update(i[0], node_record[state][2] + i[2] + heuristic(i[0], problem))
                    if node_record[i[0]][2] + node_record[i[0]][3] > node_record[state][2] + i[2] + heuristic(i[0], problem):
                        node_record[i[0]] = (state, i[1], i[2], heuristic(i[0], problem))
                        

        pop_state = priority.pop()
        node_travelled.append(pop_state)
        state = priority.heap[0][2]

    while state != initial_state:
        direction.append(node_record[state][1])
        state = node_record[state][0]

    direction.reverse()
    return direction


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
