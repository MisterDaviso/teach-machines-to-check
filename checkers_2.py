"""
Checkers Game Class v2
"""
import numpy as np
import random

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

    def newBoard(self):
        board = np.full((8,4),0)
        for i in range(len(board)):
            for j in range(len(board[i])):
                if i < 3: board[i][j] = 1
                if i > 4: board[i][j] = 2
        return board
    
    def customBoard(self,custom):
        self.board = custom

    def possibleMoves(self):
        print("The current player:",self.currentPlayer + 1)
        boardConfiguations = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] in self.pieces[self.currentPlayer]:
                    #print("Piece:",self.board[i][j])
                    boardConfiguations += self.possibleMovesForPiece(i,j,False,self.board)
        return boardConfiguations

    # Calculate all potential moves for a particular piece
    def possibleMovesForPiece(self,x,y,jumped,board):
        #if jumped: print("Made a jump. Gonna check if I can jump again.")
        yForwardChange = 1 if (x % 2 == 0) else -1
        directions = []
        if x < (len(board)-1):
            directions.append([x+1, y])
            if (y + yForwardChange) in range(len(board[x])):
                directions.append([x+1, y+yForwardChange])
        if x > 0 and board[x][y] > 2:
            directions.append([x-1,y])
            if (y - yForwardChange) in range(len(board[x])):
                directions.append([x+1, y-yForwardChange])
        
        boardConfiguations = []
        #print("Possible moves: from",x,y,"to",directions)
        for coords in directions:
            # Transpose the original table to preserve it
            variantBoard = np.copy(board)
            # Find out what is currently occupying the space
            currentOccupant = variantBoard[coords[0]][coords[1]]
            
            # If space is empty, and the piece has not jumped
            if currentOccupant == 0 and not jumped:
                #print("Moving from",x,y,"to",coords[0],coords[1])
                # Move the piece over
                variantBoard[coords[0]][coords[1]] = variantBoard[x][y]
                variantBoard[x][y] = 0
                # Check if the piece is at the end of the board and if it is kinged
                if coords[0] == (len(variantBoard) - 1) and variantBoard[coords[0]][coords[1]] <= 2:
                    variantBoard[coords[0]][coords[1]] += 2
                #print("Board after move:\n",variantBoard.T)
                # Add the configuration to the variable
                boardConfiguations.append(variantBoard)
            
            # If the space contains an enemy
            elif currentOccupant not in self.pieces[self.currentPlayer]:
                # Check if the space after is valid and empty.
                # Going forward
                if x < coords[0]:
                    checkX = coords[0]+1
                    checkY = coords[1] if coords[1] != y else y + yForwardChange
                # Going back
                else:
                    checkX = coords[0]-1
                    checkY = coords[1] if coords[1] != y else y - yForwardChange
                # Make sure the coordinates are valid
                if checkX in range(len(board)) and checkY in range(len(board[checkX])):
                    #print("Jumping from",x,y,"to",checkX,checkY)
                    # If so, make the jump and create a new configuration
                    variantBoard[checkX][checkY] = variantBoard[x][y]
                    variantBoard[coords[0]][coords[1]] = 0
                    variantBoard[x][y] = 0
                    #print("Board after jump:\n",variantBoard.T)
                    # If the piece is not a king but at the end of the board, king it
                    if checkX == (len(board)-1) and variantBoard[checkX][checkY] <= 2:
                        variantBoard[checkX][checkY] += 2
                    # If the piece is not kinged, iterate through again
                    else:
                        # Add all possible configurations to the variable.
                        print("Going to check for another jump for piece at position:",checkX,checkY,"\n",variantBoard.T)
                        boardConfiguations += self.possibleMovesForPiece(checkX,checkY,True,np.copy(variantBoard))
                    boardConfiguations.append(variantBoard)
        return boardConfiguations

    # Remember the dude from that pixar short? Yeah, let's save that guy some time.
    def flipBoard(self):
        # Turn the board into a vector
        boardVectorList = self.board.flatten().tolist()
        # Reconstruct the board in reverse order
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j] = boardVectorList.pop()

    # End the current player's turn
    def takeTurn(self,newBoard):
        # Update the board with the player's move
        self.board = newBoard
        print("The board after the player's move:\n",self.board.T)
        # Change whose turn it is
        if self.currentPlayer == 1: self.currentPlayer = 0
        else: self.currentPlayer = 1
        # Check if the game should be over
        self.gameOverConditions()
        self.flipBoard()
        print("The board before the player's move:\n",self.board.T)

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
        if self.idle >= 20: self.gameOver = True
        
        # Check if the player has any pieces remaining
        if self.p1Pieces == 0 or self.p2Pieces == 0: self.gameOver = True


# Some default arrays
arr1 = np.array([[0,2,2,2],[1,0,0,0],[2,0,0,2],[0,0,2,0],[2,0,0,1],[0,0,1,0],[0,1,1,1],[1,0,1,1]])
arr2 = np.array([[0,2,2,2],[1,0,0,0],[2,0,0,2],[0,0,2,0],[2,0,0,1],[0,0,1,0],[0,1,1,1],[1,0,1,1]])
arr3 = np.array([[1,1,0,1],[1,1,1,0],[0,1,0,0],[1,0,0,2],[0,2,1,0],[2,0,2,2],[0,0,0,0],[2,2,2,0]])

# Some practice calls
# Create a board and print it out
check = Checkers()
#check.customBoard(arr3)
# check.currentPlayer = 1
print(check.board.T)
# Create a list of potential moves and print one out
# Create a basic loop of possible moves
for i in range(10):
    variations = check.possibleMoves()
    print("There are",len(variations),"possible moves")
    check.takeTurn(variations[random.randrange(len(variations))])