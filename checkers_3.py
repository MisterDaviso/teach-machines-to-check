"""
Checkers Game Class v3
"""
import numpy as np
import random
import copy

class Checkers:
    def __init__(self):
        # While pieces are designated 1-4, the players are a binary 1 and 0
        self.currentPlayer = 0
        self.pieces = {0:[1,3], 1:[2,4]}
        self.p1Pieces = 12
        self.p2Pieces = 12
        self.board = self.newBoard()
        self.idle = 0
        self.gameOver = False
        self.directions = [[1,0], [0,1], [-1,0], [0,-1]]

    def newBoard(self):
        board = np.array([
                  [1],
                [1,1,1],
              [1,1,1,0,0],
            [1,1,1,0,0,2,2],
            [1,1,0,0,2,2,2],
              [0,0,2,2,2],
                [2,2,2],
                  [2]
        ], dtype=object)
        return board
    
    def customBoard(self,custom):
        self.board = custom

    def printBoard(self,custom=[]):
        board = self.board if len(custom) == 0 else custom
        for i in range(len(board)): 
            spaces = 3 - i if i < 4 else i - 4
            print(' ' * 3 * spaces, board[i])

    # Calculate the possible moves on a turn
    def possibleMoves(self):
        print("The current player:",self.currentPlayer + 1)
        boardConfiguations = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] in self.pieces[self.currentPlayer]:
                    boardConfiguations += self.possibleMovesForPiece(i,j,False,self.board)
        return boardConfiguations

    # Calculate all potential moves for a particular piece
    def possibleMovesForPiece(self,x,y,jumped,board):
        moves = []
        # Iterate through all possible directions
        for direction in self.directions:
            variantBoard = copy.deepcopy(board)
            # Where would that direction take you?
            xMove = x + direction[0]
            if xMove in range(len(board)):
                yMove = int(y + direction[1] + ((len(board[xMove]) - len(board[x])) / 2))
                    # The Y needs an adjustment since the columns aren't actually aligned
                # Is it a valid direction?
                if yMove in range(len(board[xMove])):
                    # Is it only going down the board/is the piece a king?
                    if direction[0] >= 0 and direction[1] >= 0 or board[x][y] > 2:
                        # Is the space there empty and has the piece yet to jump?
                        if board[xMove][yMove] == 0:
                            # Has the piece already jumped?
                            if not jumped:
                                # Move the piece
                                variantBoard[xMove][yMove] = variantBoard[x][y]
                                variantBoard[x][y] = 0
                                # If the piece has reached the other side of the board, king it
                                if xMove > 3 and yMove == (len(board[xMove]) - 1) and variantBoard[xMove][yMove] <= 2:
                                    variantBoard[xMove][yMove] += 2
                                # Add this potential move to the list
                                moves.append(variantBoard)
                        # Is the space containing an enemy?
                        elif board[xMove][yMove] not in self.pieces[self.currentPlayer]:
                            # Is the space after it valid AND empty?
                            xJump = xMove + direction[0]
                            if xJump in range(len(board)):
                                yJump = int(yMove + direction[1] + ((len(board[xJump]) - len(board[xMove])) / 2))
                                if yJump in range(len(board[xJump])) and board[xJump][yJump] == 0:
                                    # Jump your piece and remove the enemy's
                                    #print("GONNA JUMP FROM",x,y,"TO",xJump,yJump,"VALUE",variantBoard[x][y])
                                    #self.printBoard(variantBoard)
                                    variantBoard[xJump][yJump] = variantBoard[x][y]
                                    variantBoard[xMove][yMove] = variantBoard[x][y] = 0
                                    
                                    # If the piece has reached the end and isn't kinged, king it
                                    if xJump > 3 and yJump == (len(board[xJump]) - 1) and board[xJump][yJump] <= 2:
                                        variantBoard[xJump][yJump] += 2
                                    # Else, cycle back through to check for more potential jumps
                                    else:
                                        moves += self.possibleMovesForPiece(xJump,yJump,True,copy.deepcopy(variantBoard))
                                    # Add the move to the board
                                    moves.append(variantBoard)
        return moves

    # End the current player's turn
    def takeTurn(self,newBoard=[]):
        print("The current board:"); self.printBoard()
        if len(newBoard) > 0: self.board = newBoard
        print("The new board:"); self.printBoard()
        self.currentPlayer = 1 if self.currentPlayer == 0 else 0
        self.flipBoard()
        self.gameOverConditions()

    # Remember the dude from that pixar short? Yeah, let's save that guy some time.
    def flipBoard(self):
        # Reconstruct the board in reverse order
        boardCopy = copy.deepcopy(self.board)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j] = boardCopy[-(i+1)][-(j+1)]

    # Check all the conditions for a game over state
    def gameOverConditions(self):
        # Find out how many pieces are remaining on the board
        piecesOnBoard = {1:0, 2:0}
        for row in self.board:
            for piece in row:
                if piece in self.pieces[0]: piecesOnBoard[1] += 1
                if piece in self.pieces[1]: piecesOnBoard[2] += 1
        
        # If no piece has been taken, increase idle game. Otherwise, update numbers.
        if piecesOnBoard[1] == self.p1Pieces and piecesOnBoard[2] == self.p2Pieces: 
            self.idle += 1
        else: 
            self.idle = 0
            self.p1Pieces = piecesOnBoard[1]
            self.p2Pieces = piecesOnBoard[2]
        print("The game has been idle for",self.idle,"turns")
        # If no piece has been taken in 20 turns, end the game.
        if self.idle >= 50: self.gameOver = True
        
        # Check if the player has any pieces remaining
        if self.p1Pieces == 0 or self.p2Pieces == 0: self.gameOver = True


# Some practice calls
# Create a board and print it out
check = Checkers()
print(check.board[0][0])
variantBoard = copy.deepcopy(check.board)
variantBoard[0][0] = 3
print(check.board[0][0], variantBoard[0][0])
# Create a list of potential moves and print one out
# Create a basic loop of possible moves
while(not check.gameOver):
    variations = check.possibleMoves()
    print("There are",len(variations),"possible moves")
    check.takeTurn(variations[random.randrange(len(variations))]) if len(variations) > 0 else check.takeTurn()

# End of file.
