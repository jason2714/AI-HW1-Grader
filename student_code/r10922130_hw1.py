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

from turtle import done
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


    ###helper function###


    def DFS(problem, node, vis, path):

        if(problem.isGoalState(node)):
            path.insert(0, node)
            return True

        vis[node] = problem.getSuccessors(node)

        for succ in vis[node]:
            if(succ[0] not in vis):
                if DFS(problem, succ[0], vis, path):
                    path.insert(0, node)
                    return True

        return False


    ###main function###


    #declare
    path = []
    vis = {}
    ans_list = []

    #init
    start = problem.getStartState()

    if problem.isGoalState(start):
        return ans_list

    DFS(problem, start, vis, path)

    for i in range(1, len(path)):
        for item in vis[path[i-1]]:
            if(item[0] == path[i]):
                ans_list.append(item[1])
                break

    return ans_list

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"


    ###helper function###


    def BFS(problem, start, link, parent_dic):
        Q = util.Queue()

        link[start] = problem.getSuccessors(start)
        parent_dic[start] = False
        goal = None

        current = start

        while True:
            for child in link[current]: #node name as key
                if child[0] not in link:
                    parent_dic[child[0]] = current #node:parent node
                    if(problem.isGoalState(child[0])):
                        goal = child[0]
                        break
                    Q.push(child[0])
                    link[child[0]] = problem.getSuccessors(child[0]) #node:link
            if goal != None:
                break
            if Q.isEmpty():
                return False
            current = Q.pop()

        return goal


    ###main function###


    #declare
    link = {} #node:link
    parent_dic = {} #node:parent node
    ans_list = []

    #init
    start = problem.getStartState()

    if problem.isGoalState(start):
        return ans_list

    current = BFS(problem, start, link, parent_dic)

    if(current == False):
        print "Unreachable goal"

    while(current != start):
        parent = parent_dic[current]
        for linkage in link[parent]:
            if linkage[0] == current:
                ans_list.insert(0, linkage[1])
                break
        current = parent

    return ans_list



def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    def relax(u, v, cost, parent_dic, PQ, edge_cost):
        if v not in cost:
            cost[v] = cost[u] + edge_cost
            parent_dic[v] = u
            PQ.push(v, cost[v])
        elif cost[v] > (cost[u] + edge_cost):
            cost[v] = cost[u] + edge_cost
            parent_dic[v] = u
            PQ.update(v, cost[v])
        return

    def Dijk(problem, cost, parent_dic, link, PQ, end):
        while not PQ.isEmpty():
            current_node = PQ.pop()
            end.add(current_node)

            if problem.isGoalState(current_node):
                return current_node

            link[current_node] = problem.getSuccessors(current_node)
            for data in link[current_node]:
                if(data[0] not in end):
                    relax(current_node, data[0], cost, parent_dic, PQ, data[2])



    start = problem.getStartState()
    ans_list = []

    if problem.isGoalState(start):
        return ans_list

    #decalre
    PQ = util.PriorityQueue()
    cost = {}
    link = {} #node:link
    parent_dic = {} #node:parent node
    end = set()

    #init
    PQ.push(start, 0)
    parent_dic[start] = 0
    cost[start] = 0
    end.add(start)

    current_node = Dijk(problem, cost, parent_dic, link, PQ, end)

    while True:
        parent_node = parent_dic[current_node]
        for data in link[parent_node]:
            if data[0] == current_node:
                ans_list.insert(0, data[1])
                current_node = parent_node
                break
        if current_node == start:
            return ans_list


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #heuristic((1, 1), problem)
    def relax(u, v, cost, parent_dic, PQ, edge_cost, heuristic):
        if v not in cost:
            cost[v] = cost[u] + edge_cost
            parent_dic[v] = u
            PQ.push(v, cost[v] + heuristic(v, problem))
        elif cost[v] > (cost[u] + edge_cost):
            cost[v] = cost[u] + edge_cost
            parent_dic[v] = u
            PQ.update(v, cost[v] + heuristic(v, problem))
        return


    def Astar(problem, cost, parent_dic, link, PQ, end, heuristic):
        while not PQ.isEmpty():
            current_node = PQ.pop()
            end.add(current_node)

            if problem.isGoalState(current_node):
                return current_node

            link[current_node] = problem.getSuccessors(current_node)
            for data in link[current_node]:
                if(data[0] not in end):
                    relax(current_node, data[0], cost, parent_dic, PQ, data[2], heuristic)



    start = problem.getStartState()
    ans_list = []

    if problem.isGoalState(start):
        return ans_list

    #decalre
    PQ = util.PriorityQueue()
    cost = {}
    link = {} #node:link
    parent_dic = {} #node:parent node
    end = set()

    #init
    PQ.push(start, heuristic(start, problem))
    parent_dic[start] = 0
    cost[start] = 0
    end.add(start)

    current_node = Astar(problem, cost, parent_dic, link, PQ, end, heuristic)

    while True:
        parent_node = parent_dic[current_node]
        for data in link[parent_node]:
            if data[0] == current_node:
                ans_list.insert(0, data[1])
                current_node = parent_node
                break
        if current_node == start:
            return ans_list










# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
