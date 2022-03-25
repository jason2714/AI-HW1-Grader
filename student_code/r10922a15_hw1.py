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
from game import Directions

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
    # print "Start:", problem.getStartState()
    # print 
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())
    # [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
    # for i in problem.getSuccessors(problem.getStartState()):
    #     print i[0]
    #     print i[1]
    #     print i[2]
    visit = set() #record visited node
    # print visit
    path = [] #record path
    DFS(problem,problem.getStartState(),visit,path)
    #print path
    return path

def DFS(problem,node,visit,path):
    nodes = problem.getSuccessors(node)
    if len(nodes) == 0:
        return False
    visit.add(node)
    for place in nodes:

        point, direction, cost = place[0], place[1], place[2]
        # print(point)
        if point not in visit:
            path.append(direction)
            if problem.isGoalState(point):
                return True
            else:
                if DFS(problem,point,visit,path):#suceed 
                    return True
                else: #fail, remove direction
                    path.pop()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    q = util.Queue()
    q_d = util.Queue()
    visit = set(problem.getStartState())
    path = [[problem.getStartState(),0]]# ignore [point , direction]
    # direct=[]
    q.push(path)
    # q_d.push(direct)
    Final_path = []
    while(not q.isEmpty()):
        p = q.pop()
        # find solution
        #print p[:],'p[:]'
        node = p[-1][0]
        #print node,'node'
        if problem.isGoalState(node):
            Final_path=p
            break
        
        nodes = problem.getSuccessors(node)
        for place in nodes:
            point, direction, cost = place[0], place[1], place[2]
            if point not in visit:
                aaa = p[:]
                aaa.append([point,direction])
                q.push(aaa)
                visit.add(point)
    direction = []
    for i,point in enumerate(Final_path):
        if i==0:
            continue
        direction.append(point[1])
    return direction

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # check goal before node added to queue
    q = util.PriorityQueue()
    counter = util.Counter()
    counter[problem.getStartState()] = 1
    start = problem.getStartState() #[point,direction] ignore!
    backtrack = {start:start}
    # Path_Cost = {start:0} 
    Cost = {start:0} #record path cost from start to node
    nodes = {}
    # visit = set(problem.getStartState())
    visit = set()
    solution = 0
    q.update(start,0)
    Final_path = []
    while (not q.isEmpty()):
        node = q.pop()
        # node = p        
        # print node,'node'
        if problem.isGoalState(node):
            solution = node
            break
        counter[node] = 0
        visit.add(node)
        nodes[node] = problem.getSuccessors(node)
        for place in nodes[node]:
            point, direction, cost = place[0], place[1], place[2]
            cost += Cost[node]
            if point not in visit:
                # print point, direction, cost,'not in visit'
                # visit.add(point)
                # if counter[point] == 0:
                if counter[point] == 0:
                    counter[point] = 1
                    q.update(point,cost)
                    Cost[point] = cost
                    backtrack[point] = node
                elif counter[point]==1:
                    # update cost
                    if Cost[point] > cost:
                        Cost[point] = cost
                        backtrack[point] = node
                        q.update(point,cost)
            else:#node in visit
                if counter[point] > 0 and Cost[point] > cost:
                    # print point, direction, cost,'else'
                    Cost[point] = cost
                    q.update(point,cost)
                    backtrack[point] = node
    direction = []
    s = solution
    while(backtrack[s] != s):
        # print 'here'
        f = backtrack[s]
        for place in nodes[f]:
            point, d, cost = place[0], place[1], place[2]
            if point == s:
                # print point,d
                direction.append(d)
                s = f

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
    q = util.PriorityQueue()
    counter = util.Counter()
    counter[problem.getStartState()] = 1
    start = problem.getStartState() #[point,direction] ignore!
    backtrack = {start:start}
    Path_Cost = {start:0} #record path cost from start to node
    Total_Cost={start:heuristic(start,problem)} #record total path = g(n)+h(n)
    # Total_Cost={start:0} #record total path = g(n)+h(n)
    nodes = {}
    # visit = set(problem.getStartState())
    visit = set()
    solution = 0
    q.update(start,0)
    Final_path = []
    while (not q.isEmpty()):
        node = q.pop()
        # node = p        
        # print node,'node'
        if problem.isGoalState(node):
            solution = node
            break
        counter[node] = 0
        visit.add(node)
        nodes[node] = problem.getSuccessors(node)
        for place in nodes[node]:
            point, direction, cost = place[0], place[1], place[2]
            # cost = path_cost_to_node + node_to_point 
            cost += Path_Cost[node]
            if point not in visit:
                # print point, direction, cost,'not in visit'
                # visit.add(point)
                # if counter[point] == 0:
                if counter[point] == 0:
                    counter[point] = 1
                    Path_Cost[point] = cost
                    # g(n) + h(n)
                    cost += heuristic(point,problem)
                    q.update(point,cost)
                    Total_Cost[point] = cost
                    backtrack[point] = node
                elif counter[point]==1:
                    # update cost
                    if Total_Cost[point] > cost + heuristic(point,problem):
                        Total_Cost[point] = cost + heuristic(point,problem)
                        Path_Cost[point] = cost
                        backtrack[point] = node
                        q.update(point,cost)
            else:#node in visit
                if counter[point] > 0 and Total_Cost[point] > cost + heuristic(point,problem):
                    # print point, direction, cost,'else'
                    Total_Cost[point] = cost + heuristic(point,problem)
                    Path_Cost[point] = cost
                    q.update(point,cost)
                    backtrack[point] = node
    direction = []
    s = solution
    while(backtrack[s] != s):
        # print 'here'
        f = backtrack[s]
        for place in nodes[f]:
            point, d, cost = place[0], place[1], place[2]
            if point == s:
                # print point,d
                direction.append(d)
                s = f
                
    direction.reverse()
    return direction

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
