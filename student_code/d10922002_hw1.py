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
    from util import Stack
    dfs_stack = Stack()
    start_node = problem.getStartState()
    path_dict = {}#record whether visited and the path to this node(include this node)
    dfs_stack.push([start_node, None, None])# push node ,its father and dir to this node
    goal = None
    while not dfs_stack.isEmpty():
        now_node, father_node, now_dir = dfs_stack.pop()
        #check explore
        if now_node in path_dict:
            continue
        else:
            if isinstance(father_node, type(None)):
                father_path = []
            else:
                father_path = path_dict[father_node]
            now_path = list(father_path)
            if not isinstance(now_dir, type(None)):
                now_path.append(now_dir)
            path_dict[now_node] = now_path

        if problem.isGoalState(now_node):
            goal = now_node
            break

        next_list = problem.getSuccessors(now_node)
        for next_node_set in next_list:
            next_node, next_dir, next_cost = next_node_set
            if next_node not in path_dict:
                dfs_stack.push([next_node, now_node, next_dir])

    if isinstance(goal, type(None)):
        print("no goal.")
    return path_dict[goal]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    bfs_queue = Queue()
    start_node = problem.getStartState()
    path_dict = {}#record whether visited and the path to this node(include this node)
    bfs_queue.push([start_node, None, None])# push node ,its father and dir to this node
    goal = None
    while not bfs_queue.isEmpty():
        now_node, father_node, now_dir = bfs_queue.pop()
        #check explore
        if now_node in path_dict:
            continue
        else:
            if isinstance(father_node, type(None)):
                father_path = []
            else:
                father_path = path_dict[father_node]
            now_path = list(father_path)
            if not isinstance(now_dir, type(None)):
                now_path.append(now_dir)
            path_dict[now_node] = now_path

        if problem.isGoalState(now_node):
            goal = now_node
            break

        next_list = problem.getSuccessors(now_node)
        for next_node_set in next_list:
            next_node, next_dir, next_cost = next_node_set
            if next_node not in path_dict:
                bfs_queue.push([next_node, now_node, next_dir])

    if isinstance(goal, type(None)):
        print("no goal.")
    return path_dict[goal]

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    ucs_priority_queue = PriorityQueue()
    start_node = problem.getStartState()
    path_dict = {}#record whether visited and the path to this node(include this node)
    ucs_priority_queue.push([start_node, None, None, 0], 0)# push node ,its father, dir to this node and its cost
    goal = None
    while not ucs_priority_queue.isEmpty():
        test = ucs_priority_queue.pop()
        now_node, father_node, now_dir, now_path_cost = test
        #check explore
        if now_node in path_dict:
            continue
        else:
            if isinstance(father_node, type(None)):
                father_path = []
            else:
                father_path = path_dict[father_node]
            now_path = list(father_path)
            if not isinstance(now_dir, type(None)):
                now_path.append(now_dir)
            path_dict[now_node] = now_path

        if problem.isGoalState(now_node):
            goal = now_node
            break

        next_list = problem.getSuccessors(now_node)
        for next_node_set in next_list:
            next_node, next_dir, next_cost = next_node_set
            if next_node not in path_dict:
                next_path_cost = now_path_cost+next_cost
                ucs_priority_queue.update([next_node, now_node, next_dir, next_path_cost], next_path_cost)

    if isinstance(goal, type(None)):
        print("no goal.")
    return path_dict[goal]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    astar_priority_queue = PriorityQueue()
    start_node = problem.getStartState()
    path_dict = {}#record whether visited and the path to this node(include this node) and cost to this node. if new path with lower cost, update this dict
    start_future_cost = heuristic(start_node, problem)
    astar_priority_queue.push([start_node, None, None, 0], start_future_cost)# push node ,its father, dir to this node and its cost
    goal = None
    while not astar_priority_queue.isEmpty():
        test = astar_priority_queue.pop()
        now_node, father_node, now_dir, now_path_cost = test
        #check explore
        if now_node in path_dict:
            old_now_path_cost = path_dict[now_node][1]
            if old_now_path_cost<=now_path_cost:#old path is better, so skip this path
                continue
        if isinstance(father_node, type(None)):
            father_path = []
            father_cost = 0 # useless
        else:
            father_path, father_cost = path_dict[father_node]
        now_path = list(father_path)
        if not isinstance(now_dir, type(None)):
            now_path.append(now_dir)
        path_dict[now_node] = [now_path, now_path_cost]

        if problem.isGoalState(now_node):
            goal = now_node
            break

        next_list = problem.getSuccessors(now_node)
        # if len(next_list)>1:
        #     print(now_node)
        for next_node_set in next_list:
            next_node, next_dir, next_cost = next_node_set
            future_cost = heuristic(next_node, problem)
            next_path_cost = now_path_cost+next_cost
            if next_node in path_dict:#faster, but not neccessary.
                old_next_path_cost = path_dict[next_node][1]
                if old_next_path_cost<=next_path_cost:#old path is better, so skip this path
                    continue
            astar_priority_queue.update([next_node, now_node, next_dir, next_path_cost], next_path_cost+future_cost)


    if isinstance(goal, type(None)):
        print("no goal.")
    return path_dict[goal][0]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
