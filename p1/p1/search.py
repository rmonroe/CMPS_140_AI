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

  def startingState(self):
    """
    Returns the start state for the search problem
    """
    util.raiseNotDefined()

  def isGoal(self, state): #isGoal -> isGoal
    """
    state: Search state

    Returns True if and only if the state is a valid goal state
    """
    util.raiseNotDefined()

  def successorStates(self, state): #successorStates -> successorsOf
    """
    state: Search state
     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
    """
    util.raiseNotDefined()

  def actionsCost(self, actions): #actionsCost -> actionsCost
    """
      actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
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

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print "Start:", problem.startingState()
  print "Is the start a goal?", problem.isGoal(problem.startingState())
  print "Start's successors:", problem.successorStates(problem.startingState())
  """
  print "Start:", problem.startingState()
  print "Is the start a goal?", problem.isGoal(problem.startingState())
  print "Start's successors:", problem.successorStates(problem.startingState())

  # hold the fringe nodes in a stack
  fringe = util.Stack()
  # keep track of the explored nodes, to use graph search
  explored = []
  # get the starting location and path
  start = (problem.startingState(), [])
  # begin the stack with the start pos
  fringe.push(start)

  # loop until the fringe is empty
  while not fringe.isEmpty():
    #pop the first test state off the stack
    state = fringe.pop()
    #assign values for the locationa and the path to that node
    myLocation = state[0]
    myPath = state[1]

    #check that the location has not already been explored
    if(myLocation not in explored):
      # add the new location to explored
      explored.append(myLocation)
      # check if we have reached our goal
      if(problem.isGoal(myLocation)):
        return myPath
      # find the successors to this state
      successors = problem.successorStates(myLocation)
      # loop through the successors and push them onto the stack
      for i in successors:
        # but only if they havent been explored yet
        if i[0] not in explored:
          fringe.push((i[0], myPath + [i[1]]))
  return []


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  print "Start:", problem.startingState()
  print "Is the start a goal?", problem.isGoal(problem.startingState())
  print "Start's successors:", problem.successorStates(problem.startingState())

  # same implementation as DFS but with a queue for FIFO
  # hold the fringe nodes in a queue
  fringe = util.Queue()
  # keep track of the explored nodes, to use graph search
  explored = []
  # get the starting location and path
  start = (problem.startingState(), [])
  # begin the stack with the start pos
  fringe.push(start)

  # loop until the fringe is empty
  while not fringe.isEmpty():
    #pop the first test state off the stack
    state = fringe.pop()
    #assign values for the locationa and the path to that node
    myLocation = state[0]
    myPath = state[1]

    #check that the location has not already been explored
    if(myLocation not in explored):
      # add the new location to explored
      explored.append(myLocation)
      # check if we have reached our goal
      if(problem.isGoal(myLocation)):
        return myPath
      # find the successors to this state
      successors = problem.successorStates(myLocation)
      # loop through the successors and push them onto the stack
      for i in successors:
        # but only if they havent been explored yet
        if i[0] not in explored:
          fringe.push((i[0], myPath + [i[1]]))
  return []

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  print "Start:", problem.startingState()
  print "Is the start a goal?", problem.isGoal(problem.startingState())
  print "Start's successors:", problem.successorStates(problem.startingState())

  # same implementation as DFS but with a queue for FIFO
  # hold the fringe nodes in a queue
  fringe = util.PriorityQueue()
  # keep track of the explored nodes, to use graph search
  explored = []
  # get the starting location and path
  start = (problem.startingState(), [], [])
  # begin the stack with the start pos
  fringe.push(start, 0)

  # loop until the fringe is empty
  while not fringe.isEmpty():
    #pop the first test state off the stack
    state = fringe.pop()
    #assign values for the locationa and the path to that node
    myLocation = state[0]
    myPath = state[1]
    myCost = state[2]

    #check that the location has not already been explored
    if(myLocation not in explored):
      # add the new location to explored
      explored.append(myLocation)
      # check if we have reached our goal
      if(problem.isGoal(myLocation)):
        return myPath
      # find the successors to this state
      successors = problem.successorStates(myLocation)
      # loop through the successors and push them onto the stack
      for i in successors:
        # but only if they havent been explored yet
        if i[0] not in explored:
            temp = (i[0], myPath+[i[1]], myCost+[i[2]])
            fringe.push(temp, problem.actionsCost(myPath+[i[1]]))

  return []

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  print "Start:", problem.startingState()
  print "Is the start a goal?", problem.isGoal(problem.startingState())
  print "Start's successors:", problem.successorStates(problem.startingState())

  # same implementation as DFS but with a queue for FIFO
  # hold the fringe nodes in a queue
  fringe = util.PriorityQueue()
  # keep track of the explored nodes, to use graph search
  explored = []
  # get the starting location,path, and cost
  start = (problem.startingState(), [], [])
  # begin the stack with the start pos
  fringe.push(start, 0)

  # loop until the fringe is empty
  while not fringe.isEmpty():
    #pop the first test state off the stack
    state = fringe.pop()
    #assign values for the locationa and the path to that node
    myLocation = state[0]
    myPath = state[1]
    myCost = state[2]

    #check that the location has not already been explored
    if(myLocation not in explored):
      # add the new location to explored
      explored.append(myLocation)
      # check if we have reached our goal
      if(problem.isGoal(myLocation)):
        return myPath
      # find the successors to this state
      successors = problem.successorStates(myLocation)
      # loop through the successors and push them onto the stack
      for i in successors:
        # but only if they havent been explored yet
        if i[0] not in explored:
            temp = (i[0], myPath+[i[1]], myCost+[i[2]])
            fringe.push(temp, problem.actionsCost(myPath+[i[1]]) + heuristic(i[0], problem))

  return []



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
