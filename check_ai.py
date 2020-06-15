"""
Check AI
This file creates the AI that will be playing checkers
"""

# Import important libraries
import numpy as np
#import pandas as pd
#import tensorflow as tf

# Create an AI Class to keep track of everything
class CheckersAI:
    # Initialises the AI
    def __init__(self):
        # The synapses between the input, two hidden and output layers
        self.synapse_0 = 2*np.random.rand(32,4) - 1
        self.synapse_1 = 2*np.random.rand(4,4) - 1
        self.synapse_2 = 2*np.random.rand(4,1) - 1
        # The number of times the algorithm has won a match
        self.roundWins = 0
        self.totalWins = 0

    # Calculates the sigmoids of the input tensor
    def sigmoid(self, tensor):
        return 1/(1+np.exp(-tensor))

    # Calculates the slopes of the sigmoid curves
    def sigmoid_output_to_derivative(self, sigmoidTensor):
        return sigmoidTensor*(1-sigmoidTensor)

    # Determines the best possible move.
    def determineMove(self, currentBoard, potentialMoves):
        # If there are no valid moves, return the original board
        if len(potentialMoves) == 0: return currentBoard
        # Set a default for the most confident move
        mostConfidentMove = [0,0]
        # For each of the potential moves,
        for i in range(len(potentialMoves)):
            # Turn the board into a vector and save it as the input nodes
            self.input_nodes, iterator = np.empty([32]), 0
            for j in range(len(potentialMoves[i])):
                for k in range(len(potentialMoves[i][j])):
                    self.input_nodes[iterator] = potentialMoves[i][j][k]
                    iterator += 1
            # Feed the input into the neural network
            self.input_nodes = np.reshape(self.input_nodes, (1,32))
            self.layer_1 = np.reshape(self.sigmoid(np.dot(self.input_nodes,self.synapse_0)), (1,4))
            self.layer_2 = np.reshape(self.sigmoid(np.dot(self.layer_1,self.synapse_1)), (1,4))
            self.rating = self.sigmoid(np.dot(self.layer_2,self.synapse_2))
            # If the rating of the most confident is less than the current, update
            if mostConfidentMove[0] < self.rating: mostConfidentMove = [self.rating[0],i]
        # Return the potential move by the index of the most confident move
        return potentialMoves[mostConfidentMove[1]]

    # Updates the AI's synapse weights so that it may learn.
    def updateWeights(self, piecesTaken, piecesLost):
        pass

    # Updates the number of wins of the AI
    def winRound(self):
        self.roundWins += 1
        self.totalWins += 1

