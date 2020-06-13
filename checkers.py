"""
Checkers Game

This file is intended to create the game the AI will be playing with
"""

# Import necessary Libraries
import numpy as np
import random

# Create the class
class Checkers:
    # Initialize the board
    def __init__(self, random=False):
        # Two players: player 1, and player 2
        self.currentPlayer = 1
        # Set a score for both players
        self.p1Pieces = 12
        self.p2Pieces = 12
        self.moves = [
            [[1,1],[1,-1],[-1,1],[-1,-1]],
            [[-1, 1],[1, 1]],
            [[-1,-1],[1,-1]]
            ]
        self.board = self.newBoard()

    # Create a new, clean board
    def newBoard(self):
        # Invalid spaces have value None,
        # Empty spaces have value 0
        board = np.full((8,8,2),0)
            # board[i][j][k]; i=row, j=column, k=piece
        # Initialize the invalid spaces
        for i in range(len(board)):
            board[i][i%2] = board[i][i%2+2] = board[i][i%2+4] = board[i][i%2+6] = None
        # Initialize player 1
        for i in range(3):
            board[i][1-i%2][0]=board[i][3-i%2][0]=board[i][5-i%2][0]=board[i][7-i%2][0]=1
        # Initalize player 2
        for i in range(len(board)-1,len(board-4),-1):
            board[i][1-i%2][0]=board[i][3-i%2][0]=board[i][5-i%2][0]=board[i][7-i%2][0]=2
        
        return board
    
    # Create a randomized board
    def randomBoard(self):
        # Invalid spaces have value None,
        # Empty spaces have value 0
        board = np.full((8,8,2),0)
            # board[i][j][k]; i=row, j=column, k=piece
        # Initialize the invalid spaces
        for i in range(len(board)):
            board[i][i%2] = board[i][i%2+2] = board[i][i%2+4] = board[i][i%2+6] = None
        for i in range(len(board)):
            randPiece = random.choice([1,2,0,0,0,0])
            board[i][1-i%2][0]=board[i][3-i%2][0]=board[i][5-i%2][0]=board[i][7-i%2][0]=randPiece

    def possibleMoves(self):
        boardVariants = []
        # Iterate through each space on the board
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j][0] == self.currentPlayer:
                    # Find all potential moves for the current player's pieces
                    boardVariants += self.possiblePieceMoves(i,j,False,self.board)
        return boardVariants

    def possiblePieceMoves(self,x,y,jumped,board):
        # A list of possible coordinates the piece can land on
        possiblePositions = [] 
        # Determine whether the piece is a king and what moves it can make
        if board[x][y][1] == 1: possibleMoves = self.moves[0]
        else: possibleMoves = self.moves[board[x][y][0]]
        # Iterate through each potential moves
        for move in possibleMoves:
            try:
                moveX, jumpX = x+move[0], x+(2*move[0])
                moveY, jumpY = y+move[1], y+(2*move[1])
                currentPiece = board[moveX][moveY][0]
                # If a space is blank and the piece hasn't jumped, add it.
                if currentPiece == 0 and not jumped: possiblePositions.append([moveX,moveY])
                # If the space contains an enemy piece and the one after is blank, add it.
                elif currentPiece != self.currentPlayer and board[jumpX][jumpY][0] == 0:
                    possiblePositions.append([jumpX, jumpY])
            except: pass
        
        # Create new versions of boards for each potential move
        boardVariants = []
        for newPosition in possiblePositions:
            # If the piece lands on the opposite edge of the board and isn't a king, king it and move on.
            if self.currentPlayer == 1: oppositeEdge = len(self.board) - 1
            else: oppositeEdge = 0
            
            if newPosition[1] == oppositeEdge:
                # 
                pass
            # If the move was a jump, save the configuration and recurse through.
            pass
        return boardVariants
    
    # Returns the shape of the board for a possible move.
    def movePiece(self,x1,y1,x2,y2,board):
        # If the difference in one dimension is 2, it's a jump.
        if x1-x2 == 2 or x1-x2 == -2:
            
            pass
        
        # Otherwise, it's a move.
        else:
            board[x2][y2] = board[x1][y1]
            board[x1][y1] = [0,0]
    
    # Tally up how many pieces each side still has. When one has zero pieces, game over.
    def tallyPieces(self):
        pass

