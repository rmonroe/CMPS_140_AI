# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPosition = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.treeDepth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """
  # I HAVE NOT SUBMITTED THIS UNTIL NOW DUE TO COMPILING ERRORS ON MY LOCAL MACHINE.
  # I DID NOT HAVING A WORKING VERSION, TO TEST TILL NOW. I WILL BE TURNING THE ASSIGNMENT IN
  # LATE. I AM NOT TRYING TO CRAM THIS IN BEFORE THE DEADLINE
  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.treeDepth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    def max_val(state, depth, totalNumGhost):
        # terminal states
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        # arbitrarily large max to beat easily
        tempMax = -1000000

        # get pacman(max)'s move minus the STOP
        legalActions = []
        for action in state.getLegalActions(0):
            if action != Directions.STOP:
                legalActions.append(action)

        for move in legalActions:
            # send 1 to begin calculating the ghost moves, 1 is first ghost
            # send pacman successor states
            # subtract the depth by 1
            # the nummghost is the total number of ghost
            tempMax = max(tempMax, min_val(state.generateSuccessor(0,move), depth-1, 1, totalNumGhost))
        return tempMax

    def min_val(state, depth, ghost, totalNumGhost):
        # terminal states
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        # arbitrary min
        tempMin = 1000000
        # get the ghosts legal moves
        legalActions = state.getLegalActions(ghost)
        # have we done move FOR ALL ghost
        # if the ghost we are checking equal the last ghost go back to pac man
        if ghost == totalNumGhost:
            for move in legalActions:
                tempMin = min(tempMin, max_val(state.generateSuccessor(ghost,move), depth-1, totalNumGhost))
        else:
            for move in legalActions:
                # add one for next ghost
                tempMin = min(tempMin, min_val(state.generateSuccessor(ghost,move), depth-1, ghost +1, totalNumGhost))

        return tempMin

    # this makes decision minimax-Decision
    # get the legal moves for max
    legalActions = []
    for action in gameState.getLegalActions(0):
        if action != Directions.STOP:
            legalActions.append(action)
    # the number of ghost is 1 less than the total dont count pacman
    totalNumGhost = gameState.getNumAgents() - 1

    utilities = []
    # loop through max's moves
    for move in legalActions:
        # start with max(pacman) and get the successors
        nextState = gameState.generateSuccessor(0, move)
        # set the previous best
        #lastBest = utility
        # start with max
        utilities.append((min_val(nextState, self.treeDepth, 1, totalNumGhost), move))

    best = max(utilities)
    return best[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
  def getAction(self, gameState):
    """
      Returns the minimax action using self.treeDepth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    # functionally same at minimax but with alpha betas
    def max_val(state, depth, totalNumGhost, alpha, beta):
        # terminal states
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        # arbitrarily large max to beat easily
        tempMax = -1000000

        # get pacman(max)'s move minus the STOP
        legalActions = []
        for action in state.getLegalActions(0):
            if action != Directions.STOP:
                legalActions.append(action)

        for move in legalActions:
            # send 1 to begin calculating the ghost moves, 1 is first ghost
            # send pacman successor states
            # subtract the depth by 1
            # the nummghost is the total number of ghost
            tempMax = max(tempMax, min_val(state.generateSuccessor(0,move), depth-1, 1, totalNumGhost, alpha, beta))
            # handle alpha beta, is beta less than max? set alpha to the max
            if tempMax >= beta:
                return tempMax
            alpha = max(alpha, tempMax)
        return tempMax

    def min_val(state, depth, ghost, totalNumGhost, alpha, beta):
        # terminal states
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        # arbitrary min
        tempMin = 1000000
        # get the ghosts legal moves
        legalActions = state.getLegalActions(ghost)
        # have we done move FOR ALL ghost
        # if the ghost we are checking equal the last ghost go back to pac man
        if ghost == totalNumGhost:
            for move in legalActions:
                tempMin = min(tempMin, max_val(state.generateSuccessor(ghost,move), depth-1, totalNumGhost, alpha, beta))
                # is min less than alpha, stop. set beta to min
                if tempMin <= alpha:
                    return tempMin
                beta = min(beta, tempMin)
        else:
            for move in legalActions:
                # add one for next ghost
                tempMin = min(tempMin, min_val(state.generateSuccessor(ghost,move), depth-1, ghost +1, totalNumGhost, alpha, beta))
                if tempMin <= alpha:
                    return tempMin
                beta = min(beta, tempMin)
        return tempMin

    # this makes decision minimax-Decision
    # get the legal moves for max
    legalActions = []
    for action in gameState.getLegalActions(0):
        if action != Directions.STOP:
            legalActions.append(action)
    # the number of ghost is 1 less than the total dont count pacman
    totalNumGhost = gameState.getNumAgents() - 1

    utilities = []
    # arbitrary large alpha betas
    alpha = -1000000
    beta = 1000000

    # loop through max's moves
    for move in legalActions:
        # start with max(pacman) and get the successors
        nextState = gameState.generateSuccessor(0, move)
        # set the previous best
        #lastBest = utility
        # start with max
        utilities.append((min_val(nextState, self.treeDepth, 1, totalNumGhost, alpha, beta), move))

    best = max(utilities)
    return best[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.treeDepth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    def max_val(state, depth):
        # terminal states
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        # arbitrarily large max to beat easily
        tempMax = -1000000

        # get pacman(max)'s move minus the STOP
        legalActions = []
        for action in state.getLegalActions(0):
            if action != Directions.STOP:
                legalActions.append(action)

        for move in legalActions:
            lastMax = tempMax
            # send 1 to begin calculating the ghost moves, 1 is first ghost
            # send pacman successor states
            # subtract the depth by 1
            # the nummghost is the total number of ghost
            tempMax = max(tempMax, exp_val(state.generateSuccessor(0,move), depth, 1))
        return tempMax

    def exp_val(state, depth, ghost):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        legalActions = state.getLegalActions(ghost)
        tempValue = 0
        for move in legalActions:
            if ghost == (gameState.getNumAgents()-1):
                tempValue += max_val(gameState.generateSuccessor(ghost, move), depth-1)
            else:
                tempValue += exp_val(gameState.generateSuccessor(ghost, move), depth, ghost+1)
        return tempValue / len(legalActions)

    # this makes decision minimax-Decision
    # get the legal moves for max
    if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
    legalActions = []
    for action in gameState.getLegalActions(0):
        if action != Directions.STOP:
            legalActions.append(action)
    # the number of ghost is 1 less than the total dont count pacman
    utilities = []
    # loop through max's moves
    for move in legalActions:
        # start with max(pacman) and get the successors
        # set the previous best
        #lastBest = utility
        # start with max
        utilities.append((exp_val(gameState.generateSuccessor(0, move), self.treeDepth, 1), move))

    best = max(utilities)
    return best[1]

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
