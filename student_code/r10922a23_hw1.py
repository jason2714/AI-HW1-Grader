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
	
	nodes = util.Stack()
	result = util.Stack()
	
	def search(state):
		nodes.push(state)
		if problem.isGoalState(state):
			#print(nodes.list)
			return True
		
		for node in problem.getSuccessors(state):
			if node[0] not in nodes.list:
				result.push(node[1])
				if not search(node[0]):
					nodes.pop()
					result.pop()
				else:
					return True
	
	search(problem.getStartState())
	
	return result.list

def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""
	"*** YOUR CODE HERE ***"
	
	nodes = util.Queue()
	temp = util.Stack()
	visited = []
	result = []
	
	def result_parser(node):
		temp.push(node['state'][1])
		if node['parent'] is not None:
			result_parser(node['parent'])
		else:
			while not temp.isEmpty():
				action = temp.pop()
				if action is not None:
					result.append(action)
			
			return True
	
	nodes.push({'state': (problem.getStartState(), None, 0), 'parent': None})
	visited.append(problem.getStartState())
	
	while not nodes.isEmpty():
		current_node = nodes.pop()
		if problem.isGoalState(current_node['state'][0]):
			result_parser(current_node)
			return result
		
		else:
			for child_node in problem.getSuccessors(current_node['state'][0]):
				if child_node[0] not in visited:
					nodes.push({'state': child_node, 'parent': current_node})
					visited.append(child_node[0])
	#for node in problem.getSuccessors(problem.getStartState()):
	
	#util.raiseNotDefined()

def uniformCostSearch(problem):
	"""Search the node of least total cost first."""
	"*** YOUR CODE HERE ***"
	nodes = util.PriorityQueue()
	temp = util.Stack()
	visited = {}
	result = []
	
	def result_parser(node):
		temp.push(node['state'][1])
		if node['parent'] is not None:
			result_parser(node['parent'])
		else:
			while not temp.isEmpty():
				action = temp.pop()
				if action is not None:
					result.append(action)
			
			return True
	
	nodes.push({'state': (problem.getStartState(), None, 0), 'parent': None}, 0)
	
	
	while not nodes.isEmpty():
		current_node = nodes.pop()
		visited[current_node['state'][0]] = current_node['state'][2]
		
		if problem.isGoalState(current_node['state'][0]):
			result_parser(current_node)
			return result
		
		else:
			for child_node in problem.getSuccessors(current_node['state'][0]):
				new_cost = current_node['state'][2]+child_node[2]
				if child_node[0] not in visited.keys() or visited[child_node[0]] > new_cost:
					nodes.push({'state': (child_node[0], child_node[1], new_cost), 'parent': current_node}, new_cost)
					visited[child_node[0]] = new_cost
	
	#util.raiseNotDefined()

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	"*** YOUR CODE HERE ***"
	
	nodes = util.PriorityQueue()
	temp = util.Stack()
	visited = []
	result = []
	
	nodes.push({'state': (problem.getStartState(), None, 0), 'parent': None}, nullHeuristic(problem.getStartState(), problem))
	cost_f = 0
	
	def result_parser(node):
		temp.push(node['state'][1])
		if node['parent'] is not None:
			result_parser(node['parent'])
		else:
			while not temp.isEmpty():
				action = temp.pop()
				if action is not None:
					result.append(action)
			
			return True
	
	while not nodes.isEmpty():
		current_node = nodes.pop()
		if problem.isGoalState(current_node['state'][0]):
			result_parser(current_node)
			return result
			
		if current_node['state'][0] not in visited:
			for child_node in problem.getSuccessors(current_node['state'][0]):
				new_cost = current_node['state'][2] + child_node[2]
				if child_node[0] not in visited:
					nodes.push({'state': (child_node[0], child_node[1], new_cost), 'parent': current_node}, (new_cost + heuristic(child_node[0], problem)))
					
		visited.append(current_node['state'][0])
		
	#util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
