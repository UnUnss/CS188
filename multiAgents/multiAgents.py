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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        for food in prevFood.asList():
            food_distance = [manhattanDistance(newPos, food)]
            nearest_food = -min(food_distance)
        flag = True
        for ghost in newGhostStates:
            if action == 'Stop':
                flag = False
                break
            if ghost.getPosition() == newPos:
                flag = False
                break
        if flag is True:
            return nearest_food
        else:
            return -float('inf')
        # return successorGameState.getScore()
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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        Here are some method calls that might be useful when implementing minimax.
        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1
        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action
        gameState.getNumAgents():
        Returns the total number of agents in the game
        gameState.isWin():
        Returns whether or not the game state is a winning state
        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def maxValue(gameState, depth, agentIndex):
            if self.term(gameState, depth) is True:
                return self.evaluationFunction(gameState), 0
            value = -float('inf')
            for action in gameState.getLegalActions(agentIndex):
                state = gameState.generateSuccessor(agentIndex, action)
                score = minValue(state, depth, agentIndex + 1)[0]
                if score > value:
                    value = score
                    bestOption = action
            return value, bestOption

        def minValue(gameState, depth, agentIndex):
            if self.term(gameState, depth) is True:
                return self.evaluationFunction(gameState), 0
            value = float('inf')
            for action in gameState.getLegalActions(agentIndex):
                state = gameState.generateSuccessor(agentIndex, action)
                if agentIndex < gameState.getNumAgents() - 1:
                    score = minValue(state, depth, agentIndex + 1)[0]
                else:
                    score = maxValue(state, depth - 1, 0)[0]
                if score < value:
                    value = score
                    worstOption = action
            return value, worstOption
        return maxValue(gameState, self.depth - 1, 0)[1]

    def term(self, gameState, depth):
        return depth < 0 or gameState.isWin() or gameState.isLose()




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def maxValue(gameState, depth, agentIndex,alpha,beta):
            if depth < 0 or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState), 0
            value = -float('inf')
            for action in gameState.getLegalActions(agentIndex):
                score = minValue((gameState.generateSuccessor(agentIndex, action)), depth, agentIndex + 1,alpha,beta)[0]
                if score > value:
                    value = score
                    maxOption = action
                if value > beta:
                    return value, maxOption
                alpha = max(alpha, value)
            return value, maxOption

        def minValue(gameState, depth, agentIndex, alpha, beta):
            if depth < 0 or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState), 0
            value = float("inf")
            if agentIndex >= gameState.getNumAgents() - 1:
                for action in gameState.getLegalActions(agentIndex):
                    score = maxValue((gameState.generateSuccessor(agentIndex, action)), depth - 1, 0, alpha, beta)[0]
                    if score < value:
                        value = score
                        minOption = action
                    if value < alpha:
                        return value, minOption
                    beta = min(beta, value)
                return value, minOption
            else:
                for action in gameState.getLegalActions(agentIndex):
                   score = minValue((gameState.generateSuccessor(agentIndex, action)), depth, (agentIndex + 1), alpha, beta)[0]
                   if score < value:
                       value = score
                       minOption = action
                   if value < alpha:
                       return value, minOption
                   beta = min(beta, value)
                return value, minOption
        return maxValue(gameState, self.depth-1, 0, -float("inf"), float("inf"))[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction
        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectValue(gameState, self.depth, 0)[1]

    def expectValue(self, gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState), 0
            value = 0
            LegalActions = gameState.getLegalActions(agentIndex)
            Num = gameState.getNumAgents()
            if agentIndex >= gameState.getNumAgents() - 1:
                for action in gameState.getLegalActions(agentIndex):
                    state = gameState.generateSuccessor(agentIndex, action)
                    score = self.expectValue(state, depth - 1, (agentIndex + 1) % Num)[0]
                    if agentIndex == 0:
                        if score > value:
                            value = score
                            bestOption = action
                    else:
                        value += score / len(LegalActions)
                        bestOption = action
                return value, bestOption
            else:
                for action in gameState.getLegalActions(agentIndex):
                    state = gameState.generateSuccessor(agentIndex, action)
                    score = self.expectValue(state, depth, (agentIndex + 1) % Num)[0]
                    if agentIndex == 0:
                        if score > value:
                            value = score
                            bestOption = action
                    else:
                        value += score /len(LegalActions)
                        bestOption = action
                return value, bestOption


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"



# Abbreviation
better = betterEvaluationFunction
