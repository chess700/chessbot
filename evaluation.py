from copy import deepcopy
import random
import chess
import math
def engine(board,depth):
    evalboard = board.copy()
    fen = board.fen()
    blackpoint = 0
    whitepoint = 0
    evaluation = 0
    if evalboard.is_checkmate():
        if not evalboard.turn==1:
            return 1000000000000+depth
        else:
            return-10000000000-depth
    if evalboard.is_stalemate():
        return 0

    # if not evalboard.is_check():
    #     mobilityboard = deepcopy(board)
    #     mobilityboard.push(chess.Move.null())
    #     if evalboard.turn:
    #         whitepoint += len(list(evalboard.legal_moves)) / 20
    #         blackpoint += len(list(mobilityboard.legal_moves)) / 20
    #     else:
    #         blackpoint += len(list(evalboard.legal_moves)) / 20
    #         whitepoint += len(list(mobilityboard.legal_moves)) / 20

    imaginaryfen = list(evalboard.fen().split()[0])
    knightsquareindex =[0.30,0.40,0.45,0.50,0.50,0.45,0.40,0.30,
                        0.40,0.45,0.50,0.60,0.60,0.50,0.45,0.40,
                        0.65,0.80,0.85,1.00,1.00,0.85,0.80,0.65,
                        0.70,0.75,0.90,1.10,1.10,0.90,0.75,0.70,
                        0.70,0.80,0.95,1.25,1.25,0.95,0.80,0.70,
                        0.80,1.05,1.30,1.50,1.50,1.30,1.05,0.80,
                        0.65,0.70,0.85,1.00,1.00,0.85,0.70,0.65,
                        0.40,0.45,0.50,0.60,0.60,0.50,0.45,0.40]


    for squareindex,square in enumerate(chess.SQUARES):
        piece = board.piece_at(square)
        if piece is not None and piece.piece_type == chess.KNIGHT and piece.color == chess.WHITE:
            whitepoint+=(knightsquareindex[squareindex]/2)+3.5
            #whitepoint += 3
    knightsquareindex.reverse()
    for squareindex,square in enumerate(chess.SQUARES):
        piece = board.piece_at(square)
        if piece is not None and piece.piece_type == chess.KNIGHT and piece.color == chess.BLACK:
            #blackpoint+=3
            blackpoint+=(knightsquareindex[squareindex]/2)+3.5







    # print(evalboard)

    number = imaginaryfen.count('P')
    whitepoint += number
    number = imaginaryfen.count('B')
    whitepoint += number * 3
    number = imaginaryfen.count('Q')
    whitepoint += number * 9
    number = imaginaryfen.count('R')
    whitepoint += number * 5


    number = imaginaryfen.count('p')
    blackpoint += number

    number = imaginaryfen.count('b')
    blackpoint += number * 3
    number = imaginaryfen.count('q')
    blackpoint += number * 9
    number = imaginaryfen.count('r')
    blackpoint += number * 5
    # if not whitepoint+blackpoint<72:
    #     for square in chess.SQUARES:
    #         piece = board.piece_at(square)
    #         if piece is not None and piece.piece_type == chess.QUEEN and piece.color == chess.WHITE:
    #             if chess.square_rank(square)>1:
    #                 whitepoint -= 1
    #         if piece is not None and piece.piece_type == chess.QUEEN and piece.color == chess.BLACK:
    #             if chess.square_rank(square)<6:
    #                 blackpoint -=1
    if not whitepoint+blackpoint<20:
        for squareindex, square in enumerate(chess.SQUARES):
            piece = board.piece_at(square)
            if piece is not None and piece.piece_type == chess.KING and piece.color == chess.WHITE:
                whitepoint += (7-chess.square_rank(square))/2
                break


        for squareindex, square in enumerate(chess.SQUARES):
            piece = board.piece_at(square)
            if piece is not None and piece.piece_type == chess.KING and piece.color == chess.BLACK:
                blackpoint += chess.square_rank(square)-7/2
                break
    # checksforpawnonopenfile = 0
    # for squareindex, square in enumerate(chess.SQUARES):
    #     piece = board.piece_at(square)
    #     if piece is not None and piece.piece_type == chess.ROOK and piece.color == chess.BLACK:
    #         for file in chess.SQUARES:
    #             filesquare = board.piece_at(file)
    #             if (chess.square_file(file) == chess.square_file(square)) and (filesquare is not None and filesquare.piece_type == chess.PAWN and filesquare.color == chess.WHITE):
    #                 blackpoint+=5
    #                 checksforpawnonopenfile=1
    #                 break
    #         if not checksforpawnonopenfile==1:
    #             blackpoint+=6
    #         if chess.square_rank(square)==1:
    #             blackpoint+=1
    # checksforpawnonopenfile=0
    # for squareindex, square in enumerate(chess.SQUARES):
    #     piece = board.piece_at(square)
    #     if piece is not None and piece.piece_type == chess.ROOK and piece.color == chess.WHITE:
    #         for file in chess.SQUARES:
    #             filesquare= board.piece_at(file)
    #             if (chess.square_file(file) == chess.square_file(square)) and (filesquare is not None and filesquare.piece_type == chess.PAWN and filesquare.color == chess.BLACK):
    #                 whitepoint+=5
    #                 checksforpawnonopenfile=1
    #                 break
    #         if checksforpawnonopenfile==0:
    #             whitepoint+=6
    #         if chess.square_rank(square)==7:
    #             whitepoint+=1



    if whitepoint < 4:
        blackpoint += 2 * (8 - chess.square_distance(evalboard.king(chess.WHITE), evalboard.king(chess.BLACK)))/3
        blackpoint+=chess.square_manhattan_distance(evalboard.king(chess.WHITE),chess.D4)/3


    if blackpoint < 4:
        whitepoint+=chess.square_manhattan_distance(evalboard.king(chess.WHITE),chess.D4)/3



        whitepoint += 2 * (8 - chess.square_distance(evalboard.king(chess.WHITE), evalboard.king(chess.BLACK)))/3

    return round(whitepoint-blackpoint,2)+random.randint(-1,1)/100


