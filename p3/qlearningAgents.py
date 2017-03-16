# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discountRate (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
  """
  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)

    # init q values in counter again like in value iterations
    self.qVals = util.Counter()


  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
    """Description:
    Look for the state and action pair in the qvals, if not found return 0.0
    """
    """ YOUR CODE HERE """
    if not self.qVals[(state,action)]:
        return 0.0
    else:
        return self.qVals[(state,action)]
    """ END CODE """


  def getValue(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.

      break ties randomly for better behavior use random.choice()
    """
    """Description:
    If we dont have any legal actions return 0.0
    If we do then loop through them and check if best is not assigned or beaten
        if we have a new best then update it with the current value
    """
    """ YOUR CODE HERE """
    if not self.getLegalActions(state):
        return 0.0
    else:
        best = None
        for i in self.getLegalActions(state):
            temp = self.getQValue(state, i)
            if best == None or temp > best:
                best = temp
        return best
    """ END CODE """

  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.

      break ties randomly for better behavior use random.choice()
    """
    """Description:
    First, check that we have legal actions
    then we will look for the actions with the highest Q value
        if we find one we replace the best and reset the list of actions
        If we have to actions with equal value we append them to the list of best action
    we return a random selection from the list of actions
    """
    """ YOUR CODE HERE """
    if not self.getLegalActions(state):
        return None
    else:
        currentBest = None
        best = []
        for i in self.getLegalActions(state):
            temp = self.getQValue(state, i)
            if currentBest == None or temp > currentBest:
                currentBest = temp
                best = [i]
            elif temp == currentBest:
                best.append(i)
        return random.choice(best)
    """ END CODE """

  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
    # Pick Action
    legalActions = self.getLegalActions(state)
    action = None

    """Description:
    If we have no legal actions we return none, otherwise we will get a
    random choice using the conflip and epsilon or get the best policy
    """
    """ YOUR CODE HERE """
    if not legalActions:
        return None
    else:
        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        else:
            return self.getPolicy(state)
    """ END CODE """

    return action

  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    """Description:
    We will update teh qvals using the function from the temporal difference
    learning slide
    """
    """ YOUR CODE HERE """
    self.qVals[(state,action)] = ((1 - self.alpha) * self.getQValue(state,action)) + (self.alpha * (reward + (self.discountRate * self.getValue(nextState))))
    """ END CODE """

class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)

    # You might want to initialize weights here.
    self.weights = util.Counter()

  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    """Description:
    We will ge the summation of the feature values * weights
    first we loop through all keys in the feature dictionary returned from getFeatures
    we then multiply value at that key with the weight of that feature from the dict
    of weights
    """
    """ YOUR CODE HERE """
    qVal = 0
    for key in self.featExtractor.getFeatures(state, action):
        qVal += self.featExtractor.getFeatures(state, action)[key] * self.weights[key]

    return qVal
    """ END CODE """

  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
    """Description:
    We will update our weights using the correction, piece of the QLearningAgent
    update. Then we loop through all the keys in the dict from
    getFeatures again. This time though we change the weight of that key by
    doing alpha times the correction times the values of that key.
    """
    """ YOUR CODE HERE """
    correction  = (reward + (self.discountRate * self.getValue(nextState))) - self.getQValue(state,action)

    for key in self.featExtractor.getFeatures(state, action):
        self.weights[key] += (self.alpha * correction * self.featExtractor.getFeatures(state, action)[key])

    """ END CODE """

  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      util.raiseNotDefined()
