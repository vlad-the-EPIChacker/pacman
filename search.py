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

def myDFS(state,problem,prevLocations,memory):
    if problem.isGoalState(state):
        return (['Stop'],True)
    if state in prevLocations and prevLocations[state]==1:
        return ([], False)
    if state in memory.keys():
        return memory[state]

    prevLocations[state]=1
    successors=problem.getSuccessors(state)
    for i in successors:
        tempPath=myDFS(i[0],problem,prevLocations,memory)
        if tempPath[1]:
            tempPath[0].append(i[1])
            memory[state]=tempPath
            return tempPath
    prevLocations[state] = 0
    return ([],False)

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
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    path = myDFS(problem.getStartState(),problem,{},{})[0]
    path.reverse()
    return path

def myBFS(state,problem,successors):
    queue=util.Queue()
    visited={}
    queue.push((state,[]))
    while not queue.isEmpty():
        current = queue.pop()
        if problem.isGoalState(current[0]):
            current[1].append('Stop')
            return current[1]
        successors = problem.getSuccessors(current[0])
        successors.reverse()
        for i in successors:
            if str(i[0]) not in visited or visited[str(i[0])]==0:
                tempPush=(i[0],[j for j in current[1]])
                tempPush[1].append(i[1])
                visited[str(i[0])] = 1
                queue.push(tempPush)
    return state,[]


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    path=myBFS(problem.getStartState(),problem,problem.getSuccessors(problem.getStartState()))
    return path

def myDFScost(state,problem,prevLocations, cost,memory):
    if problem.isGoalState(state):
        return ([],True,cost)
    if state in prevLocations and prevLocations[state]==1:
        return ([], False,-1)
    if state in memory.keys() and memory[state][2]>-1 and cost>-1 and memory[state][2]<=cost:
        return ([], False,-1)

    prevLocations[state]=1
    successors=problem.getSuccessors(state)
    successors.reverse()
    mini=([],False,-1)
    for i in successors:
        tempPath=myDFScost(i[0],problem,prevLocations,cost+i[2],memory)
        if tempPath[1]:
            tempPath[0].append(i[1])
            if tempPath[2]<mini[2] or mini[2]==-1:
                mini=tempPath
                memory[state]=([ii for ii in tempPath[0]],True,cost)

    prevLocations[state] = 0
    return mini

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    path = myDFScost(problem.getStartState(),problem,{},0,{})[0]
    path.reverse()
    print(path)
    print("length of path:",len(path))
    return path
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def myAStarSearch(state,problem,prevLocations,cost,heuristic,memory):
    if problem.isGoalState(state):
        return (['Stop'],True,cost)
    if state in prevLocations and prevLocations[state]==1:
        return ([], False,-1)
    if state in memory.keys():
        return memory[state]

    prevLocations[state]=1
    successors=problem.getSuccessors(state)
    successors.reverse()
    priorQ = util.PriorityQueue()
    for i in successors:
        priorQ.push(i,heuristic(i[0],problem))
    while not priorQ.isEmpty():
        current=priorQ.pop()
        tempPath=myAStarSearch(current[0],problem,prevLocations,cost+current[2],heuristic,memory)
        if tempPath[1]:
            tempPath[0].append(current[1])
            memory[state] = tempPath
            return tempPath

    prevLocations[state] = 0
    return ([], False,-1)

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    path = myAStarSearch(problem.getStartState(),problem,{},0,heuristic,{})[0]
    path.reverse()
    return path
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
