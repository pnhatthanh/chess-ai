'''
    Keep DEPTH <= 4 for AI to run smoothly.

    DEPTH means the fot will looks depth moves ahead and calculate the best possible move based on PIECE-CAPTURE-SCORE AND PIECE-POSITION SCORE :
    DEPTH = 4
'''


import random
pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 2, 2, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 2, 1, 1, 2, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]


piecePositionScores = {"N": knightScores, "B": bishopScores, "Q": queenScores,
                       "R": rookScores, "wp": whitePawnScores, "bp": blackPawnScores}


CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4
SET_WHITE_AS_BOT = -1


def findRandomMoves(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove(gs, validMoves, returnQueue):
    global nextMove, whitePawnScores, blackPawnScores
    nextMove = None
    random.shuffle(validMoves)

    if gs.playerWantsToPlayAsBlack:
        # Swap the pawn score tables
        whitePawnScores, blackPawnScores = blackPawnScores, whitePawnScores

    maximizingPlayer = gs.whiteToMove  # True nếu là lượt trắng, False nếu là lượt đen

    findMoveMinimaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, maximizingPlayer)

    returnQueue.put(nextMove)
def orderMoves(gs, moves):
    moveScores = []
    for move in moves:
        score = 0
        if move.isCapture:
            capturedPiece = gs.board[move.endRow][move.endCol]
            score += pieceScore.get(capturedPiece[1], 0) * 10  
        if move in killerMoves.get(gs.MoveCount, []):
            score += 3  
        moveScores.append((score, move))
    
    moveScores.sort(reverse=True, key=lambda x: x[0])
    return [move for _, move in moveScores]

killerMoves = {}  # Lưu các nước đi mạnh

def findMoveMinimaxAlphaBeta(gs, validMoves, depth, alpha, beta, maximizingPlayer):
    global nextMove
    if depth == 0:
        return scoreBoard(gs)
    
    orderedMoves = orderMoves(gs, validMoves)  # Sắp xếp nước đi trước khi duyệt
    
    if maximizingPlayer:
        maxEval = -CHECKMATE
        for move in orderedMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            eval = findMoveMinimaxAlphaBeta(gs, nextMoves, depth - 1, alpha, beta, False)
            gs.undoMove()
            if eval > maxEval:
                maxEval = eval
                if depth == DEPTH:
                    nextMove = move
                    killerMoves[gs.MoveCount] = [move]  # Lưu move mạnh
            alpha = max(alpha, eval)
            if beta <= alpha:
                break 
        return maxEval
    else:
        minEval = CHECKMATE
        for move in orderedMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            eval = findMoveMinimaxAlphaBeta(gs, nextMoves, depth - 1, alpha, beta, True)
            gs.undoMove()
            if eval < minEval:
                minEval = eval
                if depth == DEPTH:
                    nextMove = move
                    killerMoves[gs.MoveCount] = [move]  # Lưu move mạnh
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval


def scoreBoard(gs):
    if gs.checkmate:
        return CHECKMATE if not gs.whiteToMove else -CHECKMATE
    if gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(8):
        for col in range(8):
            square = gs.board[row][col]
            if square == "--":
                continue
            pieceType = square[1]
            pieceColor = square[0]

            piecePositionScore = 0 if pieceType == "K" else piecePositionScores.get(square, [[0] * 8] * 8)[row][col]

            pieceValue = pieceScore.get(pieceType, 0) + piecePositionScore * 0.1

            if SET_WHITE_AS_BOT:
                score += pieceValue if pieceColor == 'w' else -pieceValue
            else:
                score -= pieceValue if pieceColor == 'w' else -pieceValue
    return score
'''
Positive score is good for white
Negative score is good for black
'''

# def scoreBoard(gs):
#     if gs.checkmate:
#         if gs.whiteToMove:
#             gs.checkmate = False
#             return -CHECKMATE  # black wins
#         else:
#             gs.checkmate = False
#             return CHECKMATE  # white wins
#     elif gs.stalemate:
#         return STALEMATE

#     score = 0
#     for row in range(len(gs.board)):
#         for col in range(len(gs.board[row])):
#             square = gs.board[row][col]
#             if square != "--":
#                 piecePositionScore = 0
#                 # score positionally based on piece type
#                 if square[1] != "K":
#                     # return score of the piece at that position
#                     if square[1] == "p":
#                         piecePositionScore = piecePositionScores[square][row][col]
#                     else:
#                         piecePositionScore = piecePositionScores[square[1]][row][col]
#                 if SET_WHITE_AS_BOT:
#                     if square[0] == 'w':
#                         score += pieceScore[square[1]] + \
#                             piecePositionScore * .1
#                     elif square[0] == 'b':
#                         score -= pieceScore[square[1]] + \
#                             piecePositionScore * .1
#                 else:
#                     if square[0] == 'w':
#                         score -= pieceScore[square[1]] + \
#                             piecePositionScore * .1
#                     elif square[0] == 'b':
#                         score += pieceScore[square[1]] + \
#                             piecePositionScore * .1

#     return score

