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
    state=problem.getStartState()
    L=util.Stack()
    L.__init__()
    direc=util.Stack()
    direc.__init__()
    direc2=util.Stack()
    direc2.__init__()
    st=util.Stack()
    st.__init__()
    while problem.isGoalState(state)==False:
        st.push(state)
        successors=problem.getSuccessors(state)
        su=[]
        n=len(successors)
        if n>0:
            for i in range(0,n):
                k=len(st.list)
                test=0
                for j in range(0,k):
                    if successors[i][0]==st.list[j]:
                        test=1
                if test==0:
                    su.append(successors[i])
        n2=len(su)
        
        if n2>0:
            for i in range(0,n2):
                L.push(su[i])
            s=L.pop()
            state=s[0]
            direc.push(s[1])
            direc2.push(n2)
        else:
            if direc2.isEmpty()==False:
                if direc2.list[len(direc2.list)-1]==1:
                    a=direc2.pop()
                    while a==1:
                        b=direc.pop()
                        a=direc2.pop()
                    b=direc.pop()
                else:
                    a=direc2.pop()
                    b=direc.pop()
            s=L.pop()
            state=s[0]
            direc.push(s[1])
            direc2.push(a-1)
    
    return direc.list
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    state=problem.getStartState()
    L=util.Queue()
    L.__init__()
    st=util.Queue()
    st.__init__()
    st.push(state)
    direc=util.Queue()
    direc.__init__()
    direc.push([])
    while problem.isGoalState(state)==False:
        way=direc.pop()
        successors=problem.getSuccessors(state)
        su=[]
        n=len(successors)
        if n>0:
            for i in range(0,n):
                k=len(st.list)
                test=0
                for j in range(0,k):
                    if successors[i][0]==st.list[j]:
                        test=1
                if test==0:
                    su.append(successors[i])
        n2=len(su)
        
        if n2>0:
            for i in range(0,n2):
                L.push(su[i])
                way2=way+[su[i][1]]
                direc.push(way2)
                st.push(su[i][0])
            s=L.pop()
            state=s[0]
        else:
            s=L.pop()
            state=s[0]
    way=direc.pop()
    
    return way
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    state=problem.getStartState()
    L=util.PriorityQueue()
    L.__init__()
    st=util.Stack()
    st.__init__()
    dest=util.PriorityQueue()
    dest.__init__()
    direc=util.PriorityQueue()
    stated=state
    cost=0
    way=[]
    sd=[1,[],0]
    while problem.isGoalState(state)==False:
        while (state!=stated) & (direc.isEmpty()==False):
            sd=direc.pop()
            stated=sd[0]
            cost=sd[2]
        way=sd[1]
        st.push(state)
        successors=problem.getSuccessors(state)
        su=[]
        n=len(successors)
        if n>0:
            for i in range(0,n):
                k=len(st.list)
                test=0
                for j in range(0,k):
                    if successors[i][0]==st.list[j]:
                        test=1
                if test==0:
                    su.append(successors[i])
        n2=len(su)
        if n2>0:
            for i in range(0,n2):
                cost2=cost+su[i][2]
                L.update(su[i][0],cost2)
                way2=way+[su[i][1]]
                direc.push((su[i][0],way2,cost2),cost2)
        state=L.pop()
        if problem.isGoalState(state):
            while (state!=stated) & (direc.isEmpty()==False):
                sd=direc.pop()
                stated=sd[0]
            way=sd[1]
            dest.push(way,cost)

    sol=dest.pop()
    return sol
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
    state=problem.getStartState()
    L=util.PriorityQueue()
    L.__init__()
    st=util.Stack()
    st.__init__()
    dest=util.PriorityQueue()
    dest.__init__()
    direc=util.PriorityQueue()
    stated=state
    cost=0
    way=[]
    sd=[1,[],0]
    while problem.isGoalState(state)==False:
        while (state!=stated) & (direc.isEmpty()==False):
            sd=direc.pop()
            stated=sd[0]
            cost=sd[2]
        way=sd[1]
        st.push(state)
        successors=problem.getSuccessors(state)
        su=[]
        n=len(successors)
        if n>0:
            for i in range(0,n):
                k=len(st.list)
                test=0
                for j in range(0,k):
                    if successors[i][0]==st.list[j]:
                        test=1
                if test==0:
                    su.append(successors[i])
        n2=len(su)
        if n2>0:
            for i in range(0,n2):
                cost2=cost+su[i][2]
                L.update(su[i][0],cost2+heuristic(su[i][0],problem))
                way2=way+[su[i][1]]
                direc.push((su[i][0],way2,cost2),cost2+heuristic(su[i][0],problem))
        state=L.pop()
        if problem.isGoalState(state):
            while (state!=stated) & (direc.isEmpty()==False):
                sd=direc.pop()
                stated=sd[0]
            way=sd[1]
            dest.push(way,cost)

    sol=dest.pop()
    return sol
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
