"""
The training grounds for the AI
"""
# Imported Modules
from check_ai import CheckersAI
from checkers_3 import Checkers

# Global Variables
aiPlayers = []

def aiMatch(player1,player2):
    players = [player1,player2]
    game = Checkers()
    while not game.gameOver:
        moves = game.possibleMoves()
        bestMove = players[game.currentPlayer].determineMove(game.board,moves)
        game.takeTurn(bestMove)
    #print("Score: p1 has",game.p1Pieces,"pieces left and p2 has",game.p2Pieces,"pieces left.")
    if game.p1Pieces > game.p2Pieces: player1.winRound()
    if game.p2Pieces > game.p1Pieces: player2.winRound()

def checkersAiDojo():
    # 1. Create a list of 20 AI
    for i in range(20): aiPlayers.append(CheckersAI())
    # 6. Repeat 2-5 100 times
    for p in range(10):
        # 2. Cycle through every potential pairing and pit them against each other
        for j in range(len(aiPlayers)):
            for k in range(j+1, len(aiPlayers)):
                if j != k: aiMatch(aiPlayers[j],aiPlayers[k])
        # 3. Order the list by highest round scores to lowest
        for l in range(1, len(aiPlayers)):
            for m in range(l-1, -1, -1):
                if aiPlayers[m+1].roundWins > aiPlayers[m].roundWins:
                    temp            = aiPlayers[m+1]
                    aiPlayers[m+1]  = aiPlayers[m]
                    aiPlayers[m]    = temp
                else: break
        # 4. Print out the total wins of the top 5 and reset their round wins
        print("The winners for this round have total scores of",
            aiPlayers[0].totalWins,
            aiPlayers[1].totalWins,
            aiPlayers[2].totalWins,
            aiPlayers[3].totalWins, "and",
            aiPlayers[4].totalWins,
        )
        for n in range(5):
            aiPlayers[n].roundWins = 0
        # 5. Create new 15 new ai to replace the lowest scoring ones
        for o in range(5,20): aiPlayers[o] = CheckersAI()

def aiVsHuman(ai):
    game = Checkers()
    humanTurn = int(input("Do you wish to go first (0) or second (1)?"))
    while not game.gameOver:
        if game.currentPlayer == humanTurn:
            move = game.humanMove(game.board)
            if move == "q": game.gameOver=True
            else: game.takeTurn(move)
        else:
            moves = game.possibleMoves()
            bestMove = ai.determineMove(game.board,moves)
            game.takeTurn(bestMove)

checkersAiDojo()
aiVsHuman(aiPlayers[0])

# End of file
