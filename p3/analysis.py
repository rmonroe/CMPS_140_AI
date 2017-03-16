# analysis.py
# -----------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

######################
# ANALYSIS QUESTIONS #
######################

# Change these default values to obtain the specified policies through
# value iteration.

def question2():
  answerDiscount = 0.9
  answerNoise = 0.2
  """Description:
  I dont want my agent to end up in an unintended state so, remove noise
  """
  """ YOUR CODE HERE """
  answerNoise = 0.0
  """ END CODE """
  return answerDiscount, answerNoise

def question3a():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 0.0
  """Description:
  I only want to make living hurt a little bit so I prefer the closer exit
  """
  """ YOUR CODE HERE """
  answerLivingReward = -2.0
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3b():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 0.0
  """Description:
  I want to half the discount in order to make the next state better
  and I want to make living hurt a little to prefer the closer
  """
  """ YOUR CODE HERE """
  answerDiscount = 0.5
  answerLivingReward = -1.0
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3c():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 0.0
  """Description:
  I only want to go where I intend(to avoid cliff) and I put a penalty on living
  to take the cliff path, but not enough to prefer the closer exit
  """
  """ YOUR CODE HERE """
  answerNoise = 0.0
  answerLivingReward = -1.0

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3d():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 0.0
  """Description:
  This is the path that the agent will usually follow anyway so, no need to change
  """
  """ YOUR CODE HERE """
  # no need to change anything
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3e():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 0.0
  """Description:
  I dont want to exit so I make it really good to just keep living
  """
  """ YOUR CODE HERE """
  answerLivingReward = 10.0
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question6():
  answerEpsilon = None
  answerLearningRate = None
  """Description:
  The agent will never find the optimal policy. I tried very high epsilons and
  smaller decimal epsiolns, but the agent never made it farther then halfway.
  The agent quickly discovers that the sides of the bridges are dangerous, but
  returning to the start state is more beneficial.
  """
  """ YOUR CODE HERE """
  return 'NOT POSSIBLE'
  """ END CODE """
  return answerEpsilon, answerLearningRate
  # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
  print 'Answers to analysis questions:'
  import analysis
  for q in [q for q in dir(analysis) if q.startswith('question')]:
    response = getattr(analysis, q)()
    print '  Question %s:\t%s' % (q, str(response))
