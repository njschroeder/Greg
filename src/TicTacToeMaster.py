# This is the TicTacToeMaster file within the navdeeshahuja / Python-TicTacToe-Best-Move-Generator-Artificial-Intelligence-Minimax Repository
# Apart from modifications to printBoard(), this entire file is written by them, and their account can be found at github.com/navdeeshahuja

#Copyright (c) 2017 Navdeesh Ahuja

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files 
# (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, 
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

from random import randint

def checkWin(board, player):
    for i in range(0, 7, 3):
        if(board[i] == player and board[i+1] == player and board[i+2] == player):
            return True
    for i in range(0, 3):
        if(board[i] == player and board[i+3] == player and board[i+6] == player):
            return True
    if(board[0] == player and board[4] == player and board[8] == player):
        return True
    if(board[2] == player and board[4] == player and board[6] == player):
        return True
    return False

def checkLose(board, player):
    if(player == "X"):
        opponent = "O"
    else:
        opponent = "X"
    if(checkWin(board, opponent)):
        return True
    return False
    
def checkTie(board):
    for x in board:
        if(x == " "):
            return False
    return True

def getAIMove(board, nextMove, aiPlayer):
    if(checkWin(board, aiPlayer)):
        return (-1, 10)
    elif(checkLose(board, aiPlayer)):
        return (-1, -10)
    elif(checkTie(board)):
        return (-1, -10)

    moves = []
    
    for i in range(len(board)):
        if(board[i] == " "):
            board[i] = nextMove
            
            score = getAIMove(board, ("X" if nextMove == "O" else "O"), aiPlayer)[1]
            moves.append((i, score))
            board[i] = " "

    
    if(nextMove == aiPlayer):
        maxScore = moves[0][1]
        bestMove = moves[0]
        for move in moves:
            if(move[1] > maxScore):
                bestMove = move
                maxScore = move[1]
        return bestMove
    else:
        minScore = moves[0][1]
        worstMove = moves[0]
        for move in moves:
            if(move[1] < minScore):
                worstMove = move
                minScore = move[1]
        return worstMove
        


def getRandomBoard():
    filledPositions = randint(2, 8)
    board = [" " for _ in range(9)]
    r = randint(0, 1)
    moves = ["X", "O"]
    nextMove = moves[r]
    for i in range(filledPositions):
        pos = randint(0, 8)
        while(board[pos] != " "):
            pos = randint(0, 8)
        board[pos] = nextMove
        if(nextMove == "X"):
            nextMove = "O"
        else:
            nextMove = "X"
    return (board, nextMove)

def printBoard(board):
    graphic = []
    for i in range(9):
        if(not board[i] == " "):
            graphic.append(board[i])
        else:
            graphic.append("I")
    return graphic