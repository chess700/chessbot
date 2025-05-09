import chess
import random
import evaluation
import sys
from chess import Board

sys.setrecursionlimit(1500)

cdef int positions_evaluated = 0

cdef double eval_board(BOARD, int depth=0):
    return evaluation.engine(BOARD, depth)

cdef tuple min_maxN(BOARD, int depth, double alpha, double beta, bint interativedeepening):
    global positions_evaluated

    cdef list moves = list(BOARD.legal_moves)
    cdef list forcingmoves = []

    cdef double max_eval, min_eval
    cdef tuple result
    cdef int i

    for capture_move in list(BOARD.legal_moves):
        temp = BOARD.copy()
        temp.push(capture_move)
        if BOARD.is_capture(capture_move):
            forcingmoves.append(capture_move)

    if depth < 1 and forcingmoves:
        moves = forcingmoves

    if depth > 2 and interativedeepening:
        interitivedeepeningdict = {}
        for move in moves:
            temp = BOARD.copy()
            temp.push(move)
            interitivedeepeningdict[move] = min_maxN(temp, 1, float('-inf'), float('inf'), False)[0]
        moves = list(dict(sorted(interitivedeepeningdict.items(), key=lambda item: item[1])).keys())

    if (depth < 1 and not forcingmoves) or BOARD.is_game_over() or depth < -2 or not interativedeepening:
        positions_evaluated += 1
        return eval_board(BOARD, depth), None

    best_move = None

    if BOARD.turn:  # White's turn (maximizing)
        max_eval = float('-inf')
        for move in moves:
            temp = BOARD.copy()
            temp.push(move)
            eval_score, _ = min_maxN(temp, depth - 1, alpha, beta, True)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:  # Beta cut-off
                break

        return max_eval, best_move

    else:  # Black's turn (minimizing)
        min_eval = float('inf')
        for move in moves:
            temp = BOARD.copy()
            temp.push(move)
            eval_score, _ = min_maxN(temp, depth - 1, alpha, beta, True)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:  # Alpha cut-off
                break

        return min_eval, best_move

# Wrapper function for the bot
def play_min_maxN(BOARD, int depth=2):
    global positions_evaluated
    positions_evaluated = 0

    _, best_move = min_maxN(BOARD, depth, float('-inf'), float('inf'), True)
    print("Positions evaluated:", positions_evaluated)
    print("Best move:", best_move)
    print("Eval:",_)
    return best_move
