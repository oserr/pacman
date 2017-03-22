# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()


def getCostOfActions(self, actions):
    """
    actions: A list of actions to take

    This method returns the total cost of a particular sequence of actions.
    The sequence must be composed of legal moves
    """
    util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]


class Node:
    """Defines a simple search node that does not track the cost of
    the current search path.
    """

    def __init__(self, state, actions):
        self.state = state
        self.actions = actions

    def __eq__(self, node):
        return node.state == self.state


def search(problem, strategy):
    """A generic search algorithm that can be used by DFS and BFS."""
    node = Node(problem.getStartState(), [])
    explored = set()
    strategy.push(node)
    while strategy:
        node = strategy.pop()
        if problem.isGoalState(node.state):
            return node.actions
        explored.add(node.state)
        for s, a, c in problem.getSuccessors(node.state):
            child = Node(s, node.actions+[a])
            if s not in explored and child not in strategy:
                strategy.push(child)
    return []


class CostNode:
    """Defines a simple search node that tracks the cost of the search path."""

    def __init__(self, state, actions, gcost, hcost=0):
        self.state = state
        self.actions = actions
        self.gcost = gcost
        self.hcost = hcost
        self.fcost = gcost + hcost

    def __eq__(self, node):
        return node.state == self.state

    def __le__(self, node):
        return node.fcost == self.fcost


def cost_search(problem, heuristic=lambda x,y: 0):
    """A generic search algorithm that can be used by UCS or a-star."""
    s = problem.getStartState()
    node = CostNode(s, [], 0, heuristic(s, problem))
    explored = set()
    pqueue = util.PQueue()
    pqueue.push(node)
    while pqueue:
        node = pqueue.pop()
        if problem.isGoalState(node.state):
            return node.actions
        explored.add(node.state)
        for s, a, c in problem.getSuccessors(node.state):
            hcost = heuristic(s, problem)
            gcost = node.gcost + c
            child = CostNode(s, node.actions+[a], gcost, hcost)
            if s not in explored and child not in pqueue:
                pqueue.push(child)
            elif child in pqueue:
                old_node = pqueue.get(child)
                if child.gcost < old_node.gcost:
                    pqueue.udpate(child)
    return []


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    return search(problem, util.Stack())


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    return search(problem, util.Queue())


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    node = Node(problem.getStartState(), [], 0)
    explored, frontier = set(), dict()
    frontier[node.state] = node.cost
    p_queue = util.PriorityQueue()
    p_queue.push(node, node.cost)
    while not p_queue.isEmpty():
        node = p_queue.pop()
        if problem.isGoalState(node.state):
            return node.actions
        explored.add(node.state)
        frontier.pop(node.state)
        for s, a, c in problem.getSuccessors(node.state):
            child = Node(s, node.actions+[a], node.cost+c)
            if s not in explored and s not in frontier:
                frontier[s] = child.cost
                p_queue.push(child, child.cost)
            elif s in frontier and child.cost < frontier[s]:
                frontier[s] = child.cost
                p_queue.push(child, child.cost)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    node = Node(problem.getStartState(), [], 0)
    explored, frontier = set(), dict()
    frontier[node.state] = node.cost
    p_queue = util.PriorityQueue()
    h_score = heuristic(node.state, problem)
    p_queue.push(node, node.cost+h_score)
    while not p_queue.isEmpty():
        node = p_queue.pop()
        if problem.isGoalState(node.state):
            return node.actions
        explored.add(node.state)
        frontier.pop(node.state)
        for s, a, c in problem.getSuccessors(node.state):
            child = Node(s, node.actions+[a], node.cost+c)
            if s not in explored and s not in frontier:
                frontier[s] = child.cost
                h_score = heuristic(child.state, problem)
                p_queue.push(child, child.cost+h_score)
            elif s in frontier and child.cost < frontier[s]:
                frontier[s] = child.cost
                h_score = heuristic(child.state, problem)
                p_queue.push(child, child.cost+h_score)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
