# Teach Machines To Check
This project is aimed at creating a bare-bones Checkers board game, and creating a machine learning algorithm to learn to play it.

## The Game of Checkers

### Rules


### Implementation
* To determine possible moves, cycle through each piece of the current player. 
    * For each piece, check if it's a king.
    * Check both possible moves for the piece (all 4 if king)
        * If space is empty, it can move there.
        * If there is one of your own, you cannot move there.
        * If there is an enemy piece, check if there is an empty spot opposite it.
            * If there is, jump.
            * Check if there are more adjacent enemy pieces to jump over.
                * If no more jumps can be made, return the move
    * Each potential move returns three things:
        * The board before the move takes place,
        * The board after the move takes place,
        * The number of pieces captured
            * This one may not be necessary; perhaps it best to base the move based on the board, and leave the scoring for the end.
* If moves are stored, they should be done so as: [Color, Size, [Xs, Ys], [Xe, Ye]]
    * s = start, e = end

### The Board
    X
   XXX
  --XXX
 OO--XXX
 OOO--XX
  OOO--
   OOO
    O
Hm. This version is very spartan, but it might be a bit excessive and difficult to work with.

X . X . X . X .
. X . X . X . X
X . X . X . X .
. = . = . = . =
= . = . = . = .
. O . O . O . O
O . O . O . O .
. O . O . O . O
Hm. So each move is always x+-1 but y+1 for X and y-1 for O, except if the piece is a king

## The Algorithm/Model

### Implementation
* The game will first calculate all possible moves for a given turn.
* Each possible move will be fed into the algorithm an a sigmoid scale to determine viability.
* The most viable move is implemented.
* At the end, Game calculates total pieces lost / total pieces taken, which is used as the primary source of back-propogation
    * A low ratio means the game did well, so very little needs to be updated
    * A high ratio means the game did poorly, so much needs to be updated.