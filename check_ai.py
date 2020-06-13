"""
Check AI
This file creates the AI that will be playing checkers
"""

# Import important libraries
from checkers_2 import Checkers
import numpy as np
import pandas as pd
import tensorflow as tf

# Create an AI Class to keep track of everything
class CheckersAI:
    def __init__(self):
        # Synapse 0 is [input] to [layer1]
        # synapse_0 = 2*np.random.rand(32,4) - 1
        # Synapse 1 is [layer1] to [layer2]
        # synapse_1 = 2*np.random.rand(4,4) - 1
        # Synapse 2 is [layer2] to [output]
        # synapse_2 = 2*np.random.rand(4,1) - 1
        pass

    # Calculates the sigmoids of the input tensor
    def sigmoid(self, tensor):
        return 1/(1+np.exp(-tensor))

    # Calculates the slopes of the sigmoid curves
    def sigmoid_output_to_derivative(self, sigmoidTensor):
        return sigmoidTensor*(1-sigmoidTensor)

    # Determines the best possible move.
    def determineMove(self, gameBoard, potentialMoves):
        pass

    def updateWeights(self, piecesLost, piecesTaken):
        # Calculate the ratio of pieces lost to pieces taken. 
        # A high ratio means the AI did worse and needs to improve more
        if piecesTaken > 0: score = piecesLost / piecesTaken
        else: score = piecesLost
        pass


# Create a checkers board
Game = Checkers()
print(Game.board)

# On the AI's turn, iterate through each possible move
    # The AI will take two inputs: the current board, and the potential board
    # The AI will output a rating of effectiveness for that move
    # The move with the highest rating is put into play


