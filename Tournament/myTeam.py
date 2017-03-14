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
               first = 'FinalBlitzTop', second = 'FinalBlitzBottom'):
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
  """
    These are my two agents FinalBlitzTop and FinalBlitzBottom. They are
    modified reflex agents with a very unique strategy. When thinking of a way
    to outsmart my opponent I came up with a drastic stragtegy inspired by
    Blitzkrieg or "Lightning warfare". Rather than dedicate one against to pure
    defense both of my agents think defensively on their way to the food, but
    after they become a pacman they have 1 goal consume as much food as possible.
    What makes the two agents work so well together, and the reason for the top
    bottom naming convention, is the fact that I only send each agent half of the
    foodlist. Using this method my agents do not waste moves trying to consume the
    same food as the other agent.
  """

  first = 'FinalBlitzTop'
  second = 'FinalBlitzBottom'

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########
"""
 Used the reflex agent from the example, but expanded on how it makes its
 decisions.
"""
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
        This is my agent tasked with the bottom of the foodlist, he goes for the
        bottom half of the foodlist. The strategy is mirrored in the other agent
    """
    def __init__( self, index, timeForComputing = .1 ):
        ReflexCaptureAgent.__init__( self, index, timeForComputing = .1 )

    def getFeatures(self, gameState, action):
      # perform all necessary calculations first
      features = util.Counter()
      successor = self.getSuccessor(gameState, action)
      myState = successor.getAgentState(self.index)

      # The Food Blitz, dividing the list in half
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

      # Gets a list of the opponents that are currently a ghost and those that
      # invading pacmen
      enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
      ghost = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]

      # this is this values for avoiding a ghost
      for j in ghost:
          # first get the ghost position and where he could go
          ghostPos = j.getPosition()
          ghostMoves = Actions.getLegalNeighbors(ghostPos, gameState.getWalls())
          # if I am about to hit the ghost we want to see if he is scared or not
          if (nextX, nextY) == ghostPos:
              # if the ghost is not scared we will trigger the Runaway feature
              if j.scaredTimer == 0 or (ghostPos in myMoves):
                  features['ScurdGhost'] = 0
                  features['Runaway'] = 1
              # if we made it here, he is scared and it doesn't matter, so lets
              # eat him and the food he is on
              else:
                  features['Ghostbusting'] += 1
                  features['Feast'] += 2
          # if I am in the ghost moves and he is scared I could go eat him
          elif ((nextX, nextY) in ghostMoves) and (j.scaredTimer > 0):
              features['ScurdGhost'] += 1
      # we grab powerPellets simple because they make us invicible and can eat
      # with no worry of dying
      for px, py in powerPellets:
          if nextX == px and nextY == py and myState.isPacman:
              features['ThePower'] = 1

      # this is from the reflex agent before check the score and calc the food
      features['successorScore'] = self.getScore(successor)
      if len(foodList) > 0:
          myPos = successor.getAgentState(self.index).getPosition()
          minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
          features['distanceToFood'] = minDistance # This should always be True,  but better safe than sorry
      # quick check if I am stuck
      if action==Directions.STOP:
          features['Stuck'] = 1.0

      # Here is my defensive strategy only complete this check if I am a ghost
      if not myState.isPacman:
          for j in invaders:
              # calc the moves of the invader like the ghost
              invPos = j.getPosition()
              invMoves = Actions.getLegalNeighbors(invPos, gameState.getWalls())
              # here is where I do the defensive move
              if (nextX, nextY) == invPos:
                  # if I am about to hit him and am scared we don't want to go
                  # there so we retreat
                  if myState.scaredTimer > 0:
                      features['Runaway'] = 1
                  # otherwise we want to play defensivly and eat the pacman
                  else:
                      features['Defense'] +=1
              # this is a pursue check where I only want to follow if either he
              # is in my moves or I am in his moves
              elif ((nextX, nextY) in invMoves) or (invPos in myMoves):
                  features['Pursue'] += 1
              else:
                  features['Runaway'] = 1

      return features

    # We then have to send the new weights as well
    def getWeights(self, gameState, action):
      return {'successorScore': 80, 'distanceToFood': -1, 'ScurdGhost': 3, 'Runaway': -20, 'Ghostbusting': 1, 'Feast': 2, 'ThePower': 2, 'Stuck':-100,
      'Defense':  10, 'Pursue': 5}


##################
# Blitzkrieg 2.1 #
##################
class FinalBlitzTop(ReflexCaptureAgent):
    """
        This is the mirror image of the FinalBlitzBottom agent, but he handles
        the top of the foodList, other than that they are identical in strategy.
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
      # here is where he get the other half of the food
      foodList = foodList[:half]
      powerPellets = gameState.getCapsules()

      # These all have to do with where I am and where I am going
      myPos = successor.getAgentState(self.index).getPosition()
      myX, myY = gameState.getAgentState(self.index).getPosition()
      actionX, actionY = Actions.directionToVector(action)
      nextX = int(myX + actionX)
      nextY = int(myY + actionY)
      myMoves = Actions.getLegalNeighbors((nextX,nextY), gameState.getWalls())

      # Gets a list of the opponents that are currently a ghost or pacman
      enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
      ghost = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]

      # how to handle ghost
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

      # same as base reflex agent
      features['successorScore'] = self.getScore(successor)
      if len(foodList) > 0:
          myPos = successor.getAgentState(self.index).getPosition()
          minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
          features['distanceToFood'] = minDistance # This should always be True,  but better safe than sorry
      # check that I am not stuck
      if action==Directions.STOP:
          features['Stuck'] = 1.0
      # How to play defense
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
