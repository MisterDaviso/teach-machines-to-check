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

    # Print a board according to the data model
    def printBoard(self,custom=[]):
        board = self.board if len(custom) == 0 else custom
        for i in range(len(board)): 
            spaces = 3 - i if i < 4 else i - 4
            print(' ' * 3 * spaces, board[i])

    # Print a board that is human-readable
    def printReadableBoard(self, custom=[]):
        board = self.board if len(custom) == 0 else custom
        print('  ',0,'',1,'',2,'',3,'',4,'',5,'',6,'',7)
        print(0,'',board[0][0],' - ',board[1][2],' - ',board[2][4],' - ',board[3][6],' - ')
        print(1,' - ',board[1][1],' - ',board[2][3],' - ',board[3][5],' - ',board[4][6])
        print(2,'',board[1][0],' - ',board[2][2],' - ',board[3][4],' - ',board[4][5],' - ')
        print(3,' - ',board[2][1],' - ',board[3][3],' - ',board[4][4],' - ',board[5][4])
        print(4,'',board[2][0],' - ',board[3][2],' - ',board[4][3],' - ',board[5][3],' - ')
        print(5,' - ',board[3][1],' - ',board[4][2],' - ',board[5][2],' - ',board[6][2])
        print(6,'',board[3][0],' - ',board[4][1],' - ',board[5][1],' - ',board[6][1],' - ')
        print(7,' - ',board[4][0],' - ',board[5][0],' - ',board[6][0],' - ',board[7][0])

    # Calculate the possible moves on a turn
    def possibleMoves(self):
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
        #print("The current board:"); self.printBoard()
        if len(newBoard) > 0: self.board = newBoard
        #print("The new board:"); self.printBoard()
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
        # If no piece has been taken in 20 turns, end the game.
        if self.idle >= 50: self.gameOver = True
        
        # Check if the player has any pieces remaining
        if self.p1Pieces == 0 or self.p2Pieces == 0: self.gameOver = True

    # Allow a move for human players
    def humanMove(self, board):
        self.printReadableBoard(board)
        validCoords = False
        while not validCoords:
            # In case something breaks,
            try:
                coords1 = list(map(int, input("Enter the coordinates of which piece you wish to move and where in the form 'x1,y1,x2,y2' \n").split(",")))
                # This list is to properly redirect moves made by players
                    # D1 is the row and D2 is the column
                moveMap = [
                    [[0,0],None, [1,0],None, [2,0],None, [3,0],None,],
                    [None, [1,1],None, [2,1],None, [3,1],None, [4,0]],
                    [[1,2],None, [2,2],None, [3,2],None, [4,1],None,],
                    [None, [2,3],None, [3,3],None, [4,2],None, [5,0]],
                    [[2,4],None, [3,4],None, [4,3],None, [5,1],None,],
                    [None, [3,5],None, [4,4],None, [5,2],None, [6,0]],
                    [[3,6],None, [4,5],None, [5,3],None, [6,1],None,],
                    [None, [4,6],None, [5,4],None, [6,2],None, [7,0]]
                ]
                start   = moveMap[coords1[0]][coords1[1]]
                end     = moveMap[coords1[2]][coords1[3]]
                print("This is what I have so far: input",coords1[0],coords1[1],"to",coords1[2],coords1[3],"becomes",start,"to",end)
                if coords1[2] - coords1[0] == 1 or coords1[2] - coords1[0] == -1:
                    # Move the Piece
                    board[end[0]][end[1]] = board[start[0]][start[1]]
                    board[start[0]][start[1]] = 0
                    # Don't forget to king it if it should
                    if board[end[0]][end[1]] <= 2 and coords1[2] == 7:
                        board[end[0]][end[1]] += 2
                elif coords1[2] - coords1[0] == 2 or coords1[2] - coords1[0] == -2:
                    print("Jump is being made")
                    # Make the jump
                    jumpedAdjust = (np.array(end) - np.array(start)) / 2
                    board[end[0]][end[1]] = board[start[0]][start[1]]
                    board[start[0]][start[1]] = board[start[0]+jumpedAdjust[0]][start[1]+jumpedAdjust[1]] = 0
                    # Don't forget to king it if it should
                    if board[end[0]][end[1]] <= 2 and coords1[2] == 7:
                        board[end[0]][end[1]] += 2
                else:
                    print("Something went wrong. Either you didn't move a piece or it wasn't a valid move.")
                if input("Is your turn over? (y/n) \n") == "n":
                    board = self.humanMove(copy.deepcopy(board))
                validCoords = True
            except:
                if input("Something went wrong. Do you want to exit the game? (y/n)") == 'y':
                    return 'q'
        return board

# Some practice bits
# game = Checkers()
# game.takeTurn(game.humanMove(game.board))
# game.printReadableBoard()

# End of file.
