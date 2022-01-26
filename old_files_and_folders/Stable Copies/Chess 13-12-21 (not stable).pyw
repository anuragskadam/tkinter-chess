from random import shuffle
from copy import deepcopy
from tkinter import *
# import math

gameWindow = Tk()
gameWindow.title("Chess")
gameWindow.resizable(0, 0)

SIDE_OF_WHITE = 0
# starting from bottom anti-clockwise [0, 1, 2, 3]



HORIZONTAL_VERTICAL_ARRANGEMENT_VAR = [0, 1, 0, 1][SIDE_OF_WHITE]
# 0 for horizontal, 1 for vertical
SIDE_COLOUR_VAR = [0, 0, 1, 1][SIDE_OF_WHITE]
# 0, 1 switcher

PIECE_WEIGHT_LIST = [18, 12, 10, 28, 10 ** 50, 7]

PIECES_ALIVE = [[], []]

SIDE_POINTS = [sum(PIECE_WEIGHT_LIST), sum(PIECE_WEIGHT_LIST)]


COLOUR_OF_COMPUTER = 1


CHECK_MATE_STATUS = bool(0)
PIECE_CLICK_VAR = 1000
MOVES_PLAYED = 0
LAST_MOVE = []
# [piececode, boxList index initial, boxList index final]

ENTIRE_BOARD_MATRIX = []
for r in range(8):
    ENTIRE_BOARD_MATRIX.append([])
    for c in range(8):
        ENTIRE_BOARD_MATRIX[r].append(1000)

piecesList = []
# list of all the piece instances of the class pieces (also subclass king)

boxesList = []
# list of all the box instances of the class boxes
if SIDE_COLOUR_VAR == 0:
    pieceImageList = ['Piece images\\chessBlackRook.png', 'Piece images\\chessBlackKnight.png',
                      'Piece images\\chessBlackBishop.png',
                      'Piece images\\chessBlackQueen.png', 'Piece images\\chessBlackKing.png',
                      'Piece images\\chessBlackPawn.png', 'Piece images\\chessWhiteRook.png',
                      'Piece images\\chessWhiteKnight.png',
                      'Piece images\\chessWhiteBishop.png',
                      'Piece images\\chessWhiteQueen.png', 'Piece images\\chessWhiteKing.png',
                      'Piece images\\chessWhitePawn.png']
else:
    pieceImageList = ['Piece images\\chessWhiteRook.png', 'Piece images\\chessWhiteKnight.png',
                      'Piece images\\chessWhiteBishop.png',
                      'Piece images\\chessWhiteQueen.png', 'Piece images\\chessWhiteKing.png',
                      'Piece images\\chessWhitePawn.png',
                      'Piece images\\chessBlackRook.png', 'Piece images\\chessBlackKnight.png',
                      'Piece images\\chessBlackBishop.png',
                      'Piece images\\chessBlackQueen.png', 'Piece images\\chessBlackKing.png',
                      'Piece images\\chessBlackPawn.png']

check_colour = ['salmon', 'crimson']
CHECK_MATE_COLOUR = ['grey', 'grey']
boxColourList = ['gold', 'darkred']
clickBoxColourList = ['khaki', 'darkmagenta']


class Boxes:
    def __init__(self, widget, column, row, colour, colour_occupied=3, piece_contained=1000):
        self.widget = widget
        self.colour = bool(colour)
        self.column = int(column)
        self.row = int(row)
        self.colour_occupied = colour_occupied
        self.piece_contained = piece_contained
        self.bg_colour = boxColourList[colour]

    def pieceTeleporter(self, event, victimCode=1000):
        global PIECE_CLICK_VAR, MOVES_PLAYED, LAST_MOVE, PIECES_ALIVE
        if PIECE_CLICK_VAR < 1000 and boxesList.index(self) in final_destination_giver(
                PIECE_CLICK_VAR) and victimCode == 1000 or PIECE_CLICK_VAR < 1000 and pieceCodeToPositionConverterMainBoard(
            victimCode) in final_destination_giver(PIECE_CLICK_VAR):
            # print(PIECE_CLICK_VAR)
            for i in final_destination_giver(PIECE_CLICK_VAR):
                if i != boxesList.index(self):
                    widget_highlight_remover(boxesList[i])
            if MOVES_PLAYED > 0:
                widget_colourer_and_bg_colour_attribute_setter(boxesList[LAST_MOVE[-1][1]],
                                                               boxColourList[boxesList[LAST_MOVE[-1][1]].colour])
                widget_colourer_and_bg_colour_attribute_setter(piecesList[LAST_MOVE[-1][0]],
                                                               boxColourList[boxesList[LAST_MOVE[-1][2]].colour])
            boxesList[pieceCodeToPositionConverterMainBoard(PIECE_CLICK_VAR)].colour_occupied = 3
            ENTIRE_BOARD_MATRIX[boxesList[pieceCodeToPositionConverterMainBoard(PIECE_CLICK_VAR)].column][
                boxesList[pieceCodeToPositionConverterMainBoard(PIECE_CLICK_VAR)].row] = 1000
            boxesList[pieceCodeToPositionConverterMainBoard(PIECE_CLICK_VAR)].piece_contained = 1000
            self.piece_contained = PIECE_CLICK_VAR
            boxesList[pieceCodeToPositionConverterMainBoard(PIECE_CLICK_VAR)].widget.config(
                bg=clickBoxColourList[(boxesList[pieceCodeToPositionConverterMainBoard(PIECE_CLICK_VAR)].colour)])
            LAST_MOVE.append([PIECE_CLICK_VAR, pieceCodeToPositionConverterMainBoard(PIECE_CLICK_VAR),
                              8 * self.column + self.row])
            piecesList[PIECE_CLICK_VAR].column = self.column
            piecesList[PIECE_CLICK_VAR].row = self.row

            widget_colourer_and_bg_colour_attribute_setter(piecesList[PIECE_CLICK_VAR], clickBoxColourList[
                boxesList[pieceCodeToPositionConverterMainBoard(PIECE_CLICK_VAR)].colour])

            piecesList[PIECE_CLICK_VAR].widget.grid(row=self.row, column=self.column)
            piecesList[PIECE_CLICK_VAR].movesPlayedByPiece += 1
            self.colour_occupied = int(piecesList[PIECE_CLICK_VAR].colour)
            ENTIRE_BOARD_MATRIX[self.column][self.row] = piecesList[PIECE_CLICK_VAR].pieceCode
            MOVES_PLAYED += 1

            check_checker_box_colourer()

            PIECE_CLICK_VAR = 1000

        # computer_piece_mover(computer_move_spitter())


class Pieces:
    def __init__(self, widget, typeCode, pieceCode, colour, coordinate1, coordinate2, lifeState, movesPlayedByPiece,
                 clickState=bool(0),
                 art=None, weight=0):
        self.art = art
        self.widget = widget
        self.typeCode = int(typeCode)
        self.colour = bool(colour)
        if HORIZONTAL_VERTICAL_ARRANGEMENT_VAR == 0:
            self.column = int(coordinate1)
            self.row = int(coordinate2)
        else:
            self.row = int(coordinate1)
            self.column = int(coordinate2)
        self.lifeState = lifeState
        self.movesPlayedByPiece = movesPlayedByPiece
        self.pieceCode = pieceCode
        self.clickState = clickState
        self.weight = weight

    def cursorHighlighter(self, event=None):
        if (MOVES_PLAYED + 1 + SIDE_COLOUR_VAR) % 2 == self.colour and PIECE_CLICK_VAR == 1000 and CHECK_MATE_STATUS == 0:
            widget_highlighter(self)

    def cursorHighlightRemover(self, event=None):
        if (MOVES_PLAYED + 1 + SIDE_COLOUR_VAR) % 2 == self.colour and PIECE_CLICK_VAR == 1000 and CHECK_MATE_STATUS == 0:
            widget_highlight_remover(self)

    def clickFunc(self, event):
        global PIECE_CLICK_VAR, MOVES_PLAYED
        if CHECK_MATE_STATUS == 0:
            if which_side_move() == self.colour:

                if PIECE_CLICK_VAR == 1000:
                    PIECE_CLICK_VAR = self.pieceCode
                    self.widget.config(
                        bg=clickBoxColourList[(piecesList[PIECE_CLICK_VAR].column + piecesList[PIECE_CLICK_VAR].row) % 2])
                    final_destination_giver(PIECE_CLICK_VAR)
                    for i in final_destination_giver(PIECE_CLICK_VAR):
                        widget_highlighter(boxesList[i])

                elif PIECE_CLICK_VAR == self.pieceCode:
                    self.widget.config(bg=boxesList[pieceCodeToPositionConverterMainBoard(self.pieceCode)].bg_colour)
                    boxesList[8 * self.column + self.row].widget.config(
                        bg=boxesList[pieceCodeToPositionConverterMainBoard(self.pieceCode)].bg_colour)
                    for i in final_destination_giver(PIECE_CLICK_VAR):
                        widget_highlight_remover(boxesList[i])
                    PIECE_CLICK_VAR = 1000
                else:
                    piecesList[PIECE_CLICK_VAR].widget.config(bg=boxColourList[boxesList[
                        pieceCodeToPositionConverterMainBoard(PIECE_CLICK_VAR)].colour])
                    boxesList[pieceCodeToPositionConverterMainBoard(PIECE_CLICK_VAR)].widget.config(
                        bg=boxColourList[(piecesList[PIECE_CLICK_VAR].column + piecesList[PIECE_CLICK_VAR].row) % 2])
                    for i in final_destination_giver(PIECE_CLICK_VAR):
                        widget_highlight_remover(boxesList[i])
                    PIECE_CLICK_VAR = self.pieceCode
                    self.widget.config(
                        bg=clickBoxColourList[(piecesList[PIECE_CLICK_VAR].column + piecesList[PIECE_CLICK_VAR].row) % 2])
                    boxesList[8 * self.column + self.row].widget.config(
                        bg=clickBoxColourList[(piecesList[PIECE_CLICK_VAR].column + piecesList[PIECE_CLICK_VAR].row) % 2])
                    final_destination_giver(PIECE_CLICK_VAR)
                    for i in final_destination_giver(PIECE_CLICK_VAR):
                        widget_highlighter(boxesList[i])
            elif PIECE_CLICK_VAR < 1000 and pieceCodeToPositionConverterMainBoard(
                    self.pieceCode) in final_destination_giver(PIECE_CLICK_VAR):
                self.widget.grid_remove()
                SIDE_POINTS[int(self.colour)] -= self.weight
                PIECES_ALIVE[int(self.colour)].remove(self.pieceCode)
                boxesList[pieceCodeToPositionConverterMainBoard(self.pieceCode)].pieceTeleporter(event, self.pieceCode)




class King(Pieces):
    def __init__(self, widget, typeCode, pieceCode, colour, column, row, lifeState, movesPlayedByPiece,
                 clickState=bool(0),
                 art=None, checkState=bool(0)):
        super().__init__(widget, typeCode, pieceCode, colour, column, row, lifeState, movesPlayedByPiece, art)
        self.checkState = checkState


#
#
# random use functions
def index_2d(myList, v):
    for x in myList:
        if v in x:
            return [myList.index(x), x.index(v)]


def piece_creator_function(pieceCodeInput, j_var):
    # gives pieces their icon, bg colour, and places them in grid
    piecesList[pieceCodeInput].art = PhotoImage(
        file=pieceImageList[piecesList[pieceCodeInput].typeCode + piecesList[pieceCodeInput].colour * 6])
    piecesList[pieceCodeInput].widget.config(image=piecesList[pieceCodeInput].art,
                                             bg=boxColourList[
                                                 boxesList[
                                                     pieceCodeToPositionConverterMainBoard(pieceCodeInput)].colour],
                                             width=82, height=78)
    piecesList[pieceCodeInput].widget.grid(column=piecesList[pieceCodeInput].column,
                                           row=piecesList[pieceCodeInput].row)
    ENTIRE_BOARD_MATRIX[piecesList[pieceCodeInput].column][piecesList[pieceCodeInput].row] = pieceCodeInput
    boxesList[pieceCodeToPositionConverterMainBoard(pieceCodeInput)].colour_occupied = int(
        piecesList[pieceCodeInput].colour)
    boxesList[pieceCodeToPositionConverterMainBoard(pieceCodeInput)].piece_contained = pieceCodeInput
    PIECES_ALIVE[j_var].append(pieceCodeInput)



def piececode_to_board_matrix_index_converter(pieceCodeInput, BOARD_MATRIX_INPUT=ENTIRE_BOARD_MATRIX):
    if pieceCodeInput != 1000:
        return int(
            8 * index_2d(BOARD_MATRIX_INPUT, pieceCodeInput)[0] + index_2d(BOARD_MATRIX_INPUT, pieceCodeInput)[1])


def pieceCodeToPositionConverterMainBoard(pieceCodeInput):
    # use piececode_to_board_matrix_index_converter from now on
    if pieceCodeInput != 1000:
        return int(8 * piecesList[pieceCodeInput].column + piecesList[pieceCodeInput].row)


def piece_label_default_bg_colour_giver(pieceCodeInput):
    pieceCodeInput[pieceCodeInput].widget.config(
        bg=boxColourList[boxesList[pieceCodeToPositionConverterMainBoard(pieceCodeInput)].colour])


def widget_colourer_and_bg_colour_attribute_setter(class_instance, colour):
    if class_instance in piecesList:
        class_instance.widget.config(bg=colour)
        boxesList[pieceCodeToPositionConverterMainBoard(piecesList.index(class_instance))].bg_colour = colour
    else:
        class_instance.widget.config(bg=colour)
        class_instance.bg_colour = colour


def widget_highlighter(class_instance):
    if class_instance in piecesList:
        class_instance.widget.config(bg=clickBoxColourList[(class_instance.column + class_instance.row) % 2])
    elif class_instance.piece_contained == 1000:
        class_instance.widget.config(bg=clickBoxColourList[(class_instance.column + class_instance.row) % 2])
    else:
        piecesList[class_instance.piece_contained].widget.config(
            bg=clickBoxColourList[(class_instance.column + class_instance.row) % 2])


def widget_highlight_remover(class_instance):
    if class_instance in piecesList:
        class_instance.widget.config(
            bg=boxesList[pieceCodeToPositionConverterMainBoard(class_instance.pieceCode)].bg_colour)
    elif class_instance.piece_contained == 1000:
        class_instance.widget.config(bg=class_instance.bg_colour)
    else:
        piecesList[class_instance.piece_contained].widget.config(
            bg=class_instance.bg_colour)


def boxNumberer():
    for a in boxesList:
        a.widget.config(text="{}".format(boxesList.index(a)))


def column_of_piece(pieceCode, ENTIRE_BOARD_MATRIX_INPUT=ENTIRE_BOARD_MATRIX):
    i = 0
    while pieceCode not in ENTIRE_BOARD_MATRIX_INPUT[i]:
        i += 1
    return i


def row_of_piece(pieceCode, ENTIRE_BOARD_MATRIX_INPUT=ENTIRE_BOARD_MATRIX):
    return ENTIRE_BOARD_MATRIX_INPUT[column_of_piece(pieceCode, ENTIRE_BOARD_MATRIX_INPUT)].index(pieceCode)


def box_index_to_board_matrix_element_converter(index_in_box, ENTIRE_BOARD_MATRIX_INPUT=ENTIRE_BOARD_MATRIX):
    return ENTIRE_BOARD_MATRIX_INPUT[index_in_box // 8][index_in_box % 8]


def like_coloured_piececode_list_spitter(pieceCode):
    if pieceCode in range(16):
        return list(range(16))
    else:
        return list(range(16, 32))


def king_code(colour):
    global SIDE_COLOUR_VAR
    return [[7, 23], [23, 7]][SIDE_COLOUR_VAR][colour]


def which_side_move():
    return (MOVES_PLAYED + 1 + SIDE_COLOUR_VAR) % 2

def which_side_move_w_input(moves_played_input):
    (moves_played_input + 1 + SIDE_COLOUR_VAR) % 2



def mover_for_board_matrix(piece_code_input, final_position, board_matrix = ENTIRE_BOARD_MATRIX):
    board_matrix[index_2d(board_matrix, piece_code_input)[0]][index_2d(board_matrix, piece_code_input)[1]] = 1000
    [final_position //8][final_position % 8] = piece_code_input
#probably isnt currently used


# random use functions end
#
#


def boardConstructor():
    for r in range(8):
        for c in range(8):
            boxesList.append(
                Boxes(Label(gameWindow, bg=boxColourList[(r + c) % 2], width=10, height=4), r, c,
                      (r + c) % 2))
            boxesList[8 * r + c].widget.grid(column=r, row=c)
            boxesList[8 * r + c].widget.bind("<Button-1>", boxesList[8 * r + c].pieceTeleporter)


boardConstructor()


def piece_constructor():
    pieceCodeVar = 0
    # for pieceCode
    typeCodeVar = 0
    # for typeCode
    # typeCodeVar is mostly used only for giving piece images

    piece_colour_assigner_var = [[0, 1], [1, 0]]
    for j in piece_colour_assigner_var[SIDE_COLOUR_VAR]:
        # for bnw
        # for simple pieces

        rookKnightBishopcolumn = [[0, 7], [1, 6], [2, 5]]

        for columnLoop in range(2):
            # for simple pieces
            typeCodeVar = 0

            piecesList.append(
                Pieces(Label(gameWindow),
                       typeCodeVar,
                       pieceCodeVar, bool(j), rookKnightBishopcolumn[0][columnLoop], 7 * j, bool(1), int(0), PIECE_WEIGHT_LIST[typeCodeVar]))
            piece_creator_function(pieceCodeVar, j)
            typeCodeVar += 1
            pieceCodeVar += 1

            piecesList.append(
                Pieces(Label(gameWindow),
                       typeCodeVar,
                       pieceCodeVar, bool(j), rookKnightBishopcolumn[1][columnLoop], 7 * j, bool(1), int(0), PIECE_WEIGHT_LIST[typeCodeVar]))
            piece_creator_function(pieceCodeVar, j)
            typeCodeVar += 1
            pieceCodeVar += 1

            piecesList.append(
                Pieces(Label(gameWindow),
                       typeCodeVar,
                       pieceCodeVar, bool(j), rookKnightBishopcolumn[2][columnLoop], 7 * j, bool(1), int(0), PIECE_WEIGHT_LIST[typeCodeVar]))
            piece_creator_function(pieceCodeVar, j)
            typeCodeVar += 1
            pieceCodeVar += 1

        piecesList.append(
            Pieces(Label(gameWindow), typeCodeVar,
                   pieceCodeVar, bool(j), 3, 7 * j, bool(1), int(0), PIECE_WEIGHT_LIST[typeCodeVar]))
        piece_creator_function(pieceCodeVar, j)
        typeCodeVar += 1
        pieceCodeVar += 1

        piecesList.append(
            King(Label(gameWindow), typeCodeVar,
                 pieceCodeVar, bool(j), 4, 7 * j, bool(1), int(0), PIECE_WEIGHT_LIST[typeCodeVar]))
        piece_creator_function(pieceCodeVar, j)
        typeCodeVar += 1
        pieceCodeVar += 1

        for v in range(8):
            piecesList.append(
                Pieces(Label(gameWindow), typeCodeVar, pieceCodeVar, bool(j), v, 1 + 5 * j, bool(1), int(0), PIECE_WEIGHT_LIST[typeCodeVar]))
            piece_creator_function(pieceCodeVar, j)
            pieceCodeVar += 1
        typeCodeVar += 1
    for piece in piecesList:
        piece.widget.bind("<Button-1>", piece.clickFunc)
        piece.widget.bind("<Enter>", piece.cursorHighlighter)
        piece.widget.bind("<Leave>", piece.cursorHighlightRemover)


piece_constructor()


def simple_possible_destination_giver(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT=ENTIRE_BOARD_MATRIX):
    if PIECE_CLICK_VAR < 1000:
        possibleDestinations = []
        rookBishopQueenTypeCodeList = [0, 2, 3]
        if piecesList[pieceCodeInput].typeCode in rookBishopQueenTypeCodeList:
            # rook, bishop, queen
            unitVectorList = [[[0, 1], [0, -1], [1, 0], [-1, 0]], [[1, 1], [1, -1], [-1, 1], [-1, -1]],
                              [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]]
            for v in unitVectorList[rookBishopQueenTypeCodeList.index(piecesList[pieceCodeInput].typeCode)]:
                for i in range(7):
                    # change this into a while loop
                    position = 8 * (index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[0] + (1 + i) * v[
                        0]) + index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[1] + (
                                       1 + i) * v[1]
                    if index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[0] + (1 + i) * v[0] in range(
                            8) and index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[1] + (
                            1 + i) * v[1] in range(8) and box_index_to_board_matrix_element_converter(position,
                                                                                                      ENTIRE_BOARD_MATRIX_INPUT) == 1000:
                        possibleDestinations.append(position)
                    elif index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[0] + (1 + i) * v[0] in range(
                            8) and index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[1] + (1 + i) * v[1] in range(
                        8) and box_index_to_board_matrix_element_converter(position,ENTIRE_BOARD_MATRIX_INPUT) not in like_coloured_piececode_list_spitter(
                        pieceCodeInput):
                        possibleDestinations.append(position)
                        break
                    else:
                        break
        elif piecesList[pieceCodeInput].typeCode == 1:
            # knight
            positionCheckerIndexList = [[1, -1], [2, -2]]
            for a in positionCheckerIndexList[0]:
                for b in positionCheckerIndexList[1]:
                    positionList = [[index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[0] + a,
                                     index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[1] + b],
                                    [index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[0] + b,
                                     index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[1] + a]]
                    for position in positionList:
                        if position[0] in range(8) and position[1] in range(
                                8) and box_index_to_board_matrix_element_converter(8 * position[0] + position[1],ENTIRE_BOARD_MATRIX_INPUT) not in like_coloured_piececode_list_spitter(
                            pieceCodeInput):
                            possibleDestinations.append(8 * position[0] + position[1])
        elif piecesList[pieceCodeInput].typeCode == 4:
            # king
            unitVectorList = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
            for v in unitVectorList:
                position = 8 * (column_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + v[0]) + row_of_piece(
                    pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + v[1]
                if column_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + v[0] in range(8) and row_of_piece(
                        pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + v[1] in range(
                    8) and box_index_to_board_matrix_element_converter(position,
                                                                       ENTIRE_BOARD_MATRIX_INPUT) not in like_coloured_piececode_list_spitter(
                    pieceCodeInput):
                    possibleDestinations.append(position)
        elif piecesList[pieceCodeInput].typeCode == 5:
            pawnDirectionList = [1, -1]
            pawnDirection = pawnDirectionList[piecesList[pieceCodeInput].colour]
            pawnLongitudnalCoordinate = [index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[1],
                                         index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[0]][
                HORIZONTAL_VERTICAL_ARRANGEMENT_VAR]
            pawnLateralCoordinate = [index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[0],
                                     index_2d(ENTIRE_BOARD_MATRIX_INPUT, pieceCodeInput)[1]][
                HORIZONTAL_VERTICAL_ARRANGEMENT_VAR]

            position = piececode_to_board_matrix_index_converter(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + pawnDirection * [1, 8][
                HORIZONTAL_VERTICAL_ARRANGEMENT_VAR] * 2
            if piecesList[pieceCodeInput].movesPlayedByPiece == 0 and box_index_to_board_matrix_element_converter(
                    position, ENTIRE_BOARD_MATRIX_INPUT) == 1000 and box_index_to_board_matrix_element_converter(
                position - pawnDirection * [1, 8][HORIZONTAL_VERTICAL_ARRANGEMENT_VAR],
                ENTIRE_BOARD_MATRIX_INPUT) == 1000:    # this will cause problems in singleplayer computermovespitter
                possibleDestinations.append(position)
            position = piececode_to_board_matrix_index_converter(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + pawnDirection * [1, 8][
                HORIZONTAL_VERTICAL_ARRANGEMENT_VAR]
            if box_index_to_board_matrix_element_converter(position,
                                                           ENTIRE_BOARD_MATRIX_INPUT) == 1000 and pawnLongitudnalCoordinate + pawnDirection * 1 in range(
                8):
                possibleDestinations.append(position)

            pawnColumnMovementList = [1, -1]
            for n in pawnColumnMovementList:
                position = [8, 1][HORIZONTAL_VERTICAL_ARRANGEMENT_VAR] * (pawnLateralCoordinate + n) + [1, 8][
                    HORIZONTAL_VERTICAL_ARRANGEMENT_VAR] * (pawnLongitudnalCoordinate + pawnDirection)
                if pawnLongitudnalCoordinate + pawnDirection in range(8) and pawnLateralCoordinate + n in range(
                        8) and box_index_to_board_matrix_element_converter(position, ENTIRE_BOARD_MATRIX_INPUT) not in (
                        [1000] + like_coloured_piececode_list_spitter(pieceCodeInput)):
                    possibleDestinations.append(position)

        # print(type(possibleDestinations))
        return possibleDestinations


def final_destination_giver(piece_code_input, INPUT_BOARD_MATRIX=ENTIRE_BOARD_MATRIX, INPUT_PIECES_ALIVE=PIECES_ALIVE):
    TEMP_BOARD_MATRIX = deepcopy(INPUT_BOARD_MATRIX)
    TEMP_PIECES_ALIVE = deepcopy(INPUT_PIECES_ALIVE)

    def reset_temp_board():
        nonlocal TEMP_BOARD_MATRIX, TEMP_PIECES_ALIVE
        TEMP_BOARD_MATRIX = deepcopy(INPUT_BOARD_MATRIX)
        TEMP_PIECES_ALIVE = deepcopy(INPUT_PIECES_ALIVE)

    initially_allowed_boxes = simple_possible_destination_giver(piece_code_input, TEMP_BOARD_MATRIX).copy()
    output = simple_possible_destination_giver(piece_code_input, INPUT_BOARD_MATRIX)

    for destination in initially_allowed_boxes:

        TEMP_BOARD_MATRIX[column_of_piece(piece_code_input, TEMP_BOARD_MATRIX)][
            row_of_piece(piece_code_input, TEMP_BOARD_MATRIX)] = 1000

        if TEMP_BOARD_MATRIX[destination // 8][destination % 8] in TEMP_PIECES_ALIVE[int(not piecesList[piece_code_input].colour)]:
            TEMP_PIECES_ALIVE[int(not piecesList[piece_code_input].colour)].remove(TEMP_BOARD_MATRIX[destination // 8][destination % 8])
        TEMP_BOARD_MATRIX[destination // 8][destination % 8] = piece_code_input
        for opp_piece in TEMP_PIECES_ALIVE[int(not piecesList[piece_code_input].colour)]:
            if piececode_to_board_matrix_index_converter(king_code(piecesList[piece_code_input].colour),
                                                         TEMP_BOARD_MATRIX) in simple_possible_destination_giver(
                opp_piece, TEMP_BOARD_MATRIX):
                output.remove(destination)
        reset_temp_board()

    return output


def check_checker_box_colourer():
    for i in range(2):
        truth_value = bool(0)
        for opp_piece in PIECES_ALIVE[not i]:
            if pieceCodeToPositionConverterMainBoard(king_code(i)) in simple_possible_destination_giver(opp_piece):
                widget_colourer_and_bg_colour_attribute_setter(piecesList[king_code(i)], check_colour[
                    boxesList[pieceCodeToPositionConverterMainBoard(king_code(i))].colour])
                piecesList[king_code(i)].checkState = 1
                truth_value = 1
                check_mate_checker = 1
                for piece in PIECES_ALIVE[i]:
                    if final_destination_giver(piece):
                        check_mate_checker -= 1
                        break
                if check_mate_checker == 1:
                    global CHECK_MATE_STATUS
                    CHECK_MATE_STATUS = 1
                    widget_colourer_and_bg_colour_attribute_setter(piecesList[king_code(i)], CHECK_MATE_COLOUR[i])
                    break
                    break
                break
        if truth_value == 0:
            widget_colourer_and_bg_colour_attribute_setter(piecesList[king_code(i)], boxColourList[boxesList[pieceCodeToPositionConverterMainBoard(king_code(i))].colour])
            piecesList[king_code(i)].checkState = 0

# def wieght_probability_func(weight, profitted_side):
#     def func_for_profitted_side(weight_):
#         return weight_
#     result = [1,1]
#     if profitted_side != 1000:
#
#         result[profitted_side] = func_for_profitted_side(weight)
#         result[not profitted_side] = 1 / result[profitted_side]
#
#     return result


def computer_move_spitter():
    if CHECK_MATE_STATUS == 0 and which_side_move() == COLOUR_OF_COMPUTER:
        entire_board_matrix_ = deepcopy(ENTIRE_BOARD_MATRIX)
        moves_played_ = MOVES_PLAYED
        pieces_alive_ = deepcopy(PIECES_ALIVE)
        number_of_rounds_to_check = 2
        colour_of_computer = which_side_move()
        def func_for_weight_killed_to_prob_conversion(result_for_which_colour, piece_code_killed, killer_colour):
            weight = pieceList[piece_code_killed].weight
            def func_to_use(a):
                return a
            if piece_code_killed == 1000:
                return 1
            elif result_for_which_colour == killer_colour:
                return func_to_use(weight)
            else:
                return 1 / func_to_use(weight)
        def piece_mover_in_board_matrix_and_pieces_alive_remover(piece_code_input, final_position, board_matrix_input, pieces_alive_input, colour_of_mover):
            initial_position = index_2d(board_matrix_input, piece_code_input)
            temp_board_matrix_1[initial_position[0]][initial_position[1]] = 1000
            piece_to_be_killed = temp_board_matrix_1[final_position // 8][final_position % 8]
            if piece_to_be_killed < 1000:
                pieces_alive_input[not colour_of_mover].remove(piece_to_be_killed)
            temp_board_matrix_1[final_position // 8][final_position % 8] = piece_code_input


        list_for_piece_code_and_final_position = []
        list_1 = []
        list_2 = [1000]

        for piece1 in PIECES_ALIVE[colour_of_computer]:
            temp_board_matrix_1 = deepcopy(ENTIRE_BOARD_MATRIX)
            pieces_alive_1 = deepcopy(PIECES_ALIVE)
            if piecesList[piece1].typeCode == 5:
                pawn_memory_1_original = piecesList[piece1].movesPlayedByPiece
            for move1 in final_destination_giver(piece1, temp_board_matrix_1, pieces_alive_1):
                # nonlocal temp_board_matrix_1, pieces_alive_1

                temp_board_matrix_1 = deepcopy(entire_board_matrix_)
                pieces_alive_1 = deepcopy(PIECES_ALIVE)

                l1r1 = func_for_weight_killed_to_prob_conversion(temp_board_matrix_1[move1 //8][move1 % 8])
                piece_mover_in_board_matrix_and_pieces_alive_remover(piece1, move1, temp_board_matrix_1, pieces_alive_1, pieces_alive_1)
                if piecesList[piece1].typeCode == 5:
                    piecesList[piece1].movesPlayedByPiece += 1
                for piece2 in pieces_alive_1[not colour_of_computer]:
                    # if piecesList[piece1].typeCode == 5:
                    #     pawn_memory_2_original = piecesList[piece2].movesPlayedByPiece
                    for move2 in final_destination_giver(piece2, temp_board_matrix_1, pieces_alive_1):
                        temp_board_matrix_2 = deepcopy(temp_board_matrix_1)
                        # pieces_alive_2 = deepcopy(pieces_alive_1)

                        # not needed now
                        # if piecesList[piece1].typeCode == 5:
                        #     piecesList[piece1].movesPlayedByPiece += 1
                        l1r2 = func_for_weight_killed_to_prob_conversion(temp_board_matrix_2[move2 // 8][move2 % 8])
                        l2r2 = 1 / l1r2
                        # piece_mover_in_board_matrix_and_pieces_alive_remover(piece1, move12, temp_board_matrix_1,
                        #                                                      pieces_alive_1, pieces_alive_1)
                        list_1.append(l1r1*l1r2)
                        list_2.append(l2r2)
                        list_for_piece_code_and_final_position.append([piece1, move1])
            if piecesList[piece1].typeCode == 5:
                piecesList[piece1].movesPlayedByPiece = pawn_memory_1_original


        final_list = [list_1[i] * list_2[i + 1] for i in len(list_1)]
        shuffle(final_list)
        print(list_2)
        return list_for_piece_code_and_final_position[final_list.index(max(final_list))]

    else:
        print("no")
        return 1000







def computer_piece_mover(list_w_piece_code_and_final_position):
    if list_w_piece_code_and_final_position != 1000:
        computer_move_piece_code = list_w_piece_code_and_final_position[0]
        final_position = list_w_piece_code_and_final_position[1]
        global PIECE_CLICK_VAR
        PIECE_CLICK_VAR = computer_move_piece_code
        if boxesList[final_position].colour_occupied == 3:
            boxesList[final_position].pieceTeleporter('<Key>')
        else:
            piecesList[boxesList[final_position].piece_contained].clickFunc('<Key>')
# computer_piece_mover(computer_move_spitter())

# CHECK_MATE_MOVES = [[28, 36],[12, 35],[25, 13],[5, 5],[18, 5],[4, 58],[22, 45],[6, 60],[30, 53],[8, 2],[30, 60],[8, 3],[22, 42],[9, 10],[22, 33]]
# for move in CHECK_MATE_MOVES:
#     computer_piece_mover(move)




# print("yeah")
# boxNumberer()
print(ENTIRE_BOARD_MATRIX)
# print(PIECES_ALIVE)
print(simple_possible_destination_giver(2, [[0, 8, 1000, 1000, 1000, 1000, 24, 16], [1, 9, 1000, 1000, 1000, 1000, 25, 17], [2, 10, 1000, 1000, 1000, 1000, 26, 18], [6, 11, 1000, 1000, 1000, 1000, 27, 22], [7, 12, 1000, 1000, 1000, 1000, 28, 23], [5, 13, 1000, 1000, 1000, 1000, 29, 21], [4, 14, 1000, 1000, 1000, 1000, 30, 20], [3, 15, 1000, 1000, 1000, 1000, 31, 19]]))

gameWindow.mainloop()

'''
Make single player AI game which plays w itself for some rounds and chooses the best move to play w the human opponent

Also the capabilities of the AI game fully depend on the weights given to different pieces,
so make the next level of software to make these weights accurate using neural networks
'''