# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discountRate = 0.9, iters = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discountRate = discountRate
    self.iters = iters
    self.values = util.Counter() # A Counter is a dict with default 0

    """Description:
    [Enter a description of what you did here.]
    """
    """ YOUR CODE HERE """
    # loop through the given number of iterations
    for i in range(self.iters):
        # make our own Counter
        tempVals = util.Counter()
    # loop through the possible states
        for state in self.mdp.getStates():
            best = None
            if not self.mdp.getPossibleActions(state):
                tempVals[state] = self.getValue(state)
            else:
                for action in self.mdp.getPossibleActions(state):
                    # is the new qvalue of this state better than the current best
                    if best == None or self.getQValue(state, action) > self.getQValue(state, best):
                        best = action
                tempVals[state] = self.getQValue(state, best)

        self.values = tempVals
    """ END CODE """

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]

    """Description:
    [Enter a description of what you did here.]
    """
    """ YOUR CODE HERE """
    util.raiseNotDefined()
    """ END CODE """

  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    """Description:
    have a running Qval. Then loop through the nextstates and their probabilities
    Then use the Q value equation from lecture
    Q*(s,a) = SUM T(s,a,s')[R(s,a,s') + DELTA * V*(s')]
    """
    """ YOUR CODE HERE """
    # running Qval
    Qval = 0
    # loop through states and their probs
    for nextState, transProb in self.mdp.getTransitionStatesAndProbs(state, action):
        # add to the Qval using equation from lecture
        Qval += transProb * (self.mdp.getReward(state, action,nextState) + (self.discountRate * self.getValue(nextState)))

    return Qval
    """ END CODE """

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """

    """Description:
    Loop through the possible actions and return the action with the highest Q
    value
    """
    """ YOUR CODE HERE """
    # track the best action
    best = None
    bestQ =None
    # loop through all possible action
    # this will still return none if there are no actions
    for i in self.mdp.getPossibleActions(state):
        # compute the Q values
        temp = self.getQValue(state, i)
        # has best been set yet? or is the new Q higher?
        if best == None or temp > bestQ:
            # set best to be the current action
            bestQ = temp
            best = i
    # return the best action
    return best

    """ END CODE """

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
