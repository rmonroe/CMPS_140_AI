# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util
from game import Directions, Actions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DummyAgent', second = 'DummyAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """
  first = 'FinalBlitzTop'
  second = 'FinalBlitzBottom'

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}
##################
# Blitzkrieg 2.1 #
##################
class FinalBlitzBottom(ReflexCaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """
    def __init__( self, index, timeForComputing = .1 ):
        ReflexCaptureAgent.__init__( self, index, timeForComputing = .1 )

    def getFeatures(self, gameState, action):
      features = util.Counter()
      successor = self.getSuccessor(gameState, action)
      myState = successor.getAgentState(self.index)

      # The Food Blitz still in play
      foodList = self.getFood(successor).asList()
      half = len(foodList) / 2
      foodList = foodList[half:]
      powerPellets = gameState.getCapsules()

      # These all have to do with where I am and where I am going
      myPos = successor.getAgentState(self.index).getPosition()
      myX, myY = gameState.getAgentState(self.index).getPosition()
      actionX, actionY = Actions.directionToVector(action)
      nextX = int(myX + actionX)
      nextY = int(myY + actionY)
      myMoves = Actions.getLegalNeighbors((nextX,nextY), gameState.getWalls())

      # Gets a list of the opponents that are currently a ghost
      enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
      ghost = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
      for j in ghost:
          ghostPos = j.getPosition()
          ghostMoves = Actions.getLegalNeighbors(ghostPos, gameState.getWalls())
          if (nextX, nextY) == ghostPos:
              if j.scaredTimer == 0 or (ghostPos in myMoves):
                  features['ScurdGhost'] = 0
                  features['Runaway'] = 1
              else:
                  features['Ghostbusting'] += 1
                  features['Feast'] += 2
          elif ((nextX, nextY) in ghostMoves) and (j.scaredTimer > 0):
              features['ScurdGhost'] += 1
      for px, py in powerPellets:
          if nextX == px and nextY == py and myState.isPacman:
              features['ThePower'] = 1


      features['successorScore'] = self.getScore(successor)
      if len(foodList) > 0:
          myPos = successor.getAgentState(self.index).getPosition()
          minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
          features['distanceToFood'] = minDistance # This should always be True,  but better safe than sorry
      if action==Directions.STOP:
          features['Stuck'] = 1.0

      if not myState.isPacman:
          for j in invaders:
              invPos = j.getPosition()
              invMoves = Actions.getLegalNeighbors(invPos, gameState.getWalls())

              if (nextX, nextY) == invPos:
                  if myState.scaredTimer > 0:
                      features['Runaway'] = 1
                  else:
                      features['Defense'] +=1
              elif ((nextX, nextY) in invMoves) or (invPos in myMoves):
                  features['Pursue'] += 1
              else:
                  features['Runaway'] = 1

      return features

    def getWeights(self, gameState, action):
      return {'successorScore': 80, 'distanceToFood': -1, 'ScurdGhost': 3, 'Runaway': -20, 'Ghostbusting': 1, 'Feast': 2, 'ThePower': 2, 'Stuck':-100,
      'Defense':  10, 'Pursue': 5}


##################
# Blitzkrieg 2.1 #
##################
class FinalBlitzTop(ReflexCaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """
    def __init__( self, index, timeForComputing = .1 ):
        ReflexCaptureAgent.__init__( self, index, timeForComputing = .1 )

    def getFeatures(self, gameState, action):
      features = util.Counter()
      successor = self.getSuccessor(gameState, action)
      myState = successor.getAgentState(self.index)

      # The Food Blitz still in play
      foodList = self.getFood(successor).asList()
      half = len(foodList) / 2
      foodList = foodList[:half]
      powerPellets = gameState.getCapsules()

      # These all have to do with where I am and where I am going
      myPos = successor.getAgentState(self.index).getPosition()
      myX, myY = gameState.getAgentState(self.index).getPosition()
      actionX, actionY = Actions.directionToVector(action)
      nextX = int(myX + actionX)
      nextY = int(myY + actionY)
      myMoves = Actions.getLegalNeighbors((nextX,nextY), gameState.getWalls())

      # Gets a list of the opponents that are currently a ghost
      enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
      ghost = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
      for j in ghost:
          ghostPos = j.getPosition()
          ghostMoves = Actions.getLegalNeighbors(ghostPos, gameState.getWalls())
          if (nextX, nextY) == ghostPos:
              if j.scaredTimer == 0 or (ghostPos in myMoves):
                  features['ScurdGhost'] = 0
                  features['Runaway'] = 1
              else:
                  features['Ghostbusting'] += 1
                  features['Feast'] += 2
          elif ((nextX, nextY) in ghostMoves) and (j.scaredTimer > 0):
              features['ScurdGhost'] += 1
      for px, py in powerPellets:
          if nextX == px and nextY == py and myState.isPacman:
              features['ThePower'] = 1


      features['successorScore'] = self.getScore(successor)
      if len(foodList) > 0:
          myPos = successor.getAgentState(self.index).getPosition()
          minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
          features['distanceToFood'] = minDistance # This should always be True,  but better safe than sorry
      if action==Directions.STOP:
          features['Stuck'] = 1.0

      if not myState.isPacman:
          for j in invaders:
              invPos = j.getPosition()
              invMoves = Actions.getLegalNeighbors(invPos, gameState.getWalls())
              if (nextX, nextY) == invPos:
                  features['Defense'] =1
              elif ((nextX, nextY) in invMoves) and (myState.scaredTimer > 0):
                  features['Runaway'] = 1
              else:
                  features['Pursue'] += 1

      return features

    def getWeights(self, gameState, action):
      return {'successorScore': 80, 'distanceToFood': -1, 'ScurdGhost': 3, 'Runaway': -20, 'Ghostbusting': 1, 'Feast': 2, 'ThePower': 2, 'Stuck':-100,
      'Defense':  2, 'Pursue': 1}




##################
# Blitzkrieg 2.0 #
##################
class BlitzSmartBottom(ReflexCaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """
    def __init__( self, index, timeForComputing = .1 ):
        ReflexCaptureAgent.__init__( self, index, timeForComputing = .1 )

    def getFeatures(self, gameState, action):
      features = util.Counter()
      successor = self.getSuccessor(gameState, action)
      myState = successor.getAgentState(self.index)

      # The Food Blitz still in play
      foodList = self.getFood(successor).asList()
      half = len(foodList) / 2
      foodList = foodList[:half]
      powerPellets = gameState.getCapsules()

      # These all have to do with where I am and where I am going
      myPos = successor.getAgentState(self.index).getPosition()
      myX, myY = gameState.getAgentState(self.index).getPosition()
      actionX, actionY = Actions.directionToVector(action)
      nextX = int(myX + actionX)
      nextY = int(myY + actionY)

      # Gets a list of the opponents that are currently a ghost
      enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
      ghost = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      # invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
      for j in ghost:
          ghostPos = j.getPosition()
          ghostMoves = Actions.getLegalNeighbors(ghostPos, gameState.getWalls())
          if (nextX, nextY) == ghostPos:
              if j.scaredTimer == 0:
                  features['ScurdGhost'] = 0
                  features['Runaway'] = 1
              else:
                  features['Ghostbusting'] += 1
                  features['Feast'] += 2
          elif ((nextX, nextY) in ghostMoves) and (j.scaredTimer > 0):
              features['ScurdGhost'] += 1
      for px, py in powerPellets:
          if nextX == px and nextY == py and myState.isPacman:
              features['ThePower'] = 1

      features['successorScore'] = self.getScore(successor)
      if len(foodList) > 0:
          myPos = successor.getAgentState(self.index).getPosition()
          minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
          features['distanceToFood'] = minDistance # This should always be True,  but better safe than sorry
      if action==Directions.STOP:
          features['Stuck'] = 1.0

      return features

    def getWeights(self, gameState, action):
      return {'successorScore': 80, 'distanceToFood': -1, 'ScurdGhost': 3, 'Runaway': -20, 'Ghostbusting': 1, 'Feast': 2, 'ThePower': 2, 'Stuck':-100}



class BlitzSmartTop(ReflexCaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """
    def getFeatures(self, gameState, action):
      features = util.Counter()
      successor = self.getSuccessor(gameState, action)
      myState = successor.getAgentState(self.index)

      # The Food Blitz still in play
      foodList = self.getFood(successor).asList()
      half = len(foodList) / 2
      foodList = foodList[half:]
      powerPellets = gameState.getCapsules()

      # These all have to do with where I am and where I am going
      myPos = successor.getAgentState(self.index).getPosition()
      myX, myY = gameState.getAgentState(self.index).getPosition()
      actionX, actionY = Actions.directionToVector(action)
      nextX = int(myX + actionX)
      nextY = int(myY + actionY)

      # Gets a list of the opponents that are currently a ghost
      enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
      ghost = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      # invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
      for j in ghost:
          ghostPos = j.getPosition()
          ghostMoves = Actions.getLegalNeighbors(ghostPos, gameState.getWalls())
          if (nextX, nextY) == ghostPos:
              if j.scaredTimer == 0:
                  features['ScurdGhost'] = 0
                  features['Runaway'] = 1
              else:
                  features['Ghostbusting'] += 2
                  features['Feast'] += 1
          elif ((nextX, nextY) in ghostMoves) and (j.scaredTimer > 0):
              print("DONT CARE")
              features['ScurdGhost'] += 1

      for px, py in powerPellets:
          if nextX == px and nextY == py and myState.isPacman:
              features['ThePower'] = 1
      features['successorScore'] = self.getScore(successor)
      if len(foodList) > 0:
          myPos = successor.getAgentState(self.index).getPosition()
          minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
          features['distanceToFood'] = minDistance# This should always be True,  but better safe than sorry
      if action==Directions.STOP:
          features["stuck"] = 1.0

      return features

    def getWeights(self, gameState, action):
      return {'successorScore': 80, 'distanceToFood': -1, 'ScurdGhost': 3, 'Runaway': -20, 'Ghostbusting': 1, 'Feast': 2, 'ThePower': 2, 'Stuck':-100}



class SanteDefense(ReflexCaptureAgent):
    """
    A reflex agent that keeps its side Pacman-free. Again,
    this is to give you an idea of what a defensive agent
    could be like.  It is not the best or only way to make
    such an agent.
    """

    def getFeatures(self, gameState, action):
      features = util.Counter()
      successor = self.getSuccessor(gameState, action)

      myState = successor.getAgentState(self.index)
      myPos = myState.getPosition()

      # Computes whether we're on defense (1) or offense (0)
      features['onDefense'] = 1
      if myState.isPacman: features['onDefense'] = 0

      # Computes distance to invaders we can see
      enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
      invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
      features['numInvaders'] = len(invaders)
      if len(invaders) > 0:
        dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
        features['invaderDistance'] = min(dists)

      if action == Directions.STOP: features['stop'] = 1
      rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
      if action == rev: features['reverse'] = 1

      return features

    def getWeights(self, gameState, action):
      return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}



##############
# Blitzkrieg #
##############
"""
The idea behind this team is to simply improve the reflex agent and overwhelm
the opponent. This is done, but blitzing the opponent and sending both agents
on offense. But rather than have both agents go for the same food the "bottom"
agent is tasked with the first set of the food list and vis versa for the top.
Double offense seems logical given the time/move limits

Win Rate vs. Baseline: ~70%
"""
class BlitzBottom(ReflexCaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """
    def getFeatures(self, gameState, action):
      features = util.Counter()
      successor = self.getSuccessor(gameState, action)
      features['successorScore'] = self.getScore(successor)

      # Compute distance to the nearest food
      foodList = self.getFood(successor).asList()
      half = len(foodList) / 2
      foodList = foodList[:half]
      if len(foodList) > 0: # This should always be True,  but better safe than sorry
        myPos = successor.getAgentState(self.index).getPosition()
        minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
        features['distanceToFood'] = minDistance
      return features

    def getWeights(self, gameState, action):
      return {'successorScore': 100, 'distanceToFood': -1}
class BlitzTop(ReflexCaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """
    def getFeatures(self, gameState, action):
      features = util.Counter()
      successor = self.getSuccessor(gameState, action)
      features['successorScore'] = self.getScore(successor)

      # Compute distance to the nearest food
      foodList = self.getFood(successor).asList()
      half = len(foodList) / 2
      foodList = foodList[half:]
      if len(foodList) > 0: # This should always be True,  but better safe than sorry
        myPos = successor.getAgentState(self.index).getPosition()
        minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
        features['distanceToFood'] = minDistance
      return features

    def getWeights(self, gameState, action):
      return {'successorScore': 100, 'distanceToFood': -1}


class SanteDefense(ReflexCaptureAgent):
    """
    A reflex agent that keeps its side Pacman-free. Again,
    this is to give you an idea of what a defensive agent
    could be like.  It is not the best or only way to make
    such an agent.
    """

    def getFeatures(self, gameState, action):
      features = util.Counter()
      successor = self.getSuccessor(gameState, action)

      myState = successor.getAgentState(self.index)
      myPos = myState.getPosition()

      # Computes whether we're on defense (1) or offense (0)
      features['onDefense'] = 1
      if myState.isPacman: features['onDefense'] = 0

      # Computes distance to invaders we can see
      enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
      invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
      features['numInvaders'] = len(invaders)
      if len(invaders) > 0:
        dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
        features['invaderDistance'] = min(dists)

      if action == Directions.STOP: features['stop'] = 1
      rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
      if action == rev: features['reverse'] = 1

      return features

    def getWeights(self, gameState, action):
      return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}



class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    return random.choice(actions)
