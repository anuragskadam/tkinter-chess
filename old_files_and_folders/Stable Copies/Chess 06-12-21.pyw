from tkinter import *
from copy import deepcopy

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

    def pieceTeleporter(self, event, victimCode=1000):
        global PIECE_CLICK_VAR, MOVES_PLAYED, LAST_MOVE
        if PIECE_CLICK_VAR < 1000 and boxesList.index(self) in final_destination_giver(
                PIECE_CLICK_VAR) and victimCode == 1000 or PIECE_CLICK_VAR < 1000 and pieceCodeToPositionConverterMainBoard(
            victimCode) in final_destination_giver(PIECE_CLICK_VAR):
            for i in final_destination_giver(PIECE_CLICK_VAR):
                if i != boxesList.index(self):
                    widget_highlight_remover(boxesList[i])
            if MOVES_PLAYED > 0:
                boxesList[LAST_MOVE[-1][1]].widget.config(bg=boxColourList[boxesList[LAST_MOVE[-1][1]].colour])
                piecesList[LAST_MOVE[-1][0]].widget.config(bg=boxColourList[boxesList[LAST_MOVE[-1][2]].colour])

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

            piecesList[PIECE_CLICK_VAR].widget.config(
                bg=clickBoxColourList[boxesList[pieceCodeToPositionConverterMainBoard(PIECE_CLICK_VAR)].colour])
            piecesList[PIECE_CLICK_VAR].widget.grid(row=self.row, column=self.column)
            piecesList[PIECE_CLICK_VAR].movesPlayedByPiece += 1
            self.colour_occupied = int(piecesList[PIECE_CLICK_VAR].colour)
            ENTIRE_BOARD_MATRIX[self.column][self.row] = piecesList[PIECE_CLICK_VAR].pieceCode

            PIECE_CLICK_VAR = 1000
            MOVES_PLAYED += 1



class Pieces:
    def __init__(self, widget, typeCode, pieceCode, colour, coordinate1, coordinate2, lifeState, movesPlayedByPiece,
                 clickState=bool(0),
                 art=None):
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

    def cursorHighlighter(self, event=None):
        if (MOVES_PLAYED + 1 + SIDE_COLOUR_VAR) % 2 == self.colour and PIECE_CLICK_VAR == 1000:
            widget_highlighter(self)

    def cursorHighlightRemover(self, event=None):
        if (MOVES_PLAYED + 1 + SIDE_COLOUR_VAR) % 2 == self.colour and PIECE_CLICK_VAR == 1000:
            widget_highlight_remover(self)

    def clickFunc(self, event):
        global PIECE_CLICK_VAR, MOVES_PLAYED
        if which_side_move() == self.colour:

            if PIECE_CLICK_VAR == 1000:
                PIECE_CLICK_VAR = self.pieceCode
                self.widget.config(
                    bg=clickBoxColourList[(piecesList[PIECE_CLICK_VAR].column + piecesList[PIECE_CLICK_VAR].row) % 2])
                final_destination_giver(PIECE_CLICK_VAR)
                for i in final_destination_giver(PIECE_CLICK_VAR):
                    widget_highlighter(boxesList[i])

            elif PIECE_CLICK_VAR == self.pieceCode:
                self.widget.config(bg=boxColourList[boxesList[
                    pieceCodeToPositionConverterMainBoard(PIECE_CLICK_VAR)].colour])
                boxesList[8 * self.column + self.row].widget.config(bg=boxColourList[boxesList[
                    pieceCodeToPositionConverterMainBoard(PIECE_CLICK_VAR)].colour])
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
            SIDE_POINTS[int(self.colour)] -= PIECE_WEIGHT_LIST[self.typeCode]
            PIECES_ALIVE[int(self.colour)].remove(self.pieceCode)
            boxesList[pieceCodeToPositionConverterMainBoard(self.pieceCode)].pieceTeleporter(event, self.pieceCode)
            self.row = 1000
            self.column = 1000


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
                                                 boxesList[pieceCodeToPositionConverterMainBoard(pieceCodeInput)].colour],
                                             width=82, height=78)
    piecesList[pieceCodeInput].widget.grid(column=piecesList[pieceCodeInput].column,
                                           row=piecesList[pieceCodeInput].row)
    ENTIRE_BOARD_MATRIX[piecesList[pieceCodeInput].column][piecesList[pieceCodeInput].row] = pieceCodeInput
    boxesList[pieceCodeToPositionConverterMainBoard(pieceCodeInput)].colour_occupied = int(piecesList[pieceCodeInput].colour)
    boxesList[pieceCodeToPositionConverterMainBoard(pieceCodeInput)].piece_contained = pieceCodeInput
    PIECES_ALIVE[j_var].append(pieceCodeInput)

def piececode_to_board_matrix_index_converter(pieceCodeInput, BOARD_MATRIX_INPUT = ENTIRE_BOARD_MATRIX):
    if pieceCodeInput != 1000:
        return int(8 * index_2d(BOARD_MATRIX_INPUT, pieceCodeInput)[0] + index_2d(BOARD_MATRIX_INPUT, pieceCodeInput)[1])


def pieceCodeToPositionConverterMainBoard(pieceCodeInput):
    if pieceCodeInput != 1000:
        return int(8 * piecesList[pieceCodeInput].column + piecesList[pieceCodeInput].row)


def piece_label_default_bg_colour_giver(pieceCodeInput):
    pieceCodeInput[pieceCodeInput].widget.config(
        bg=boxColourList[boxesList[pieceCodeToPositionConverterMainBoard(pieceCodeInput)].colour])


def widget_highlighter(classAttribute):
    if classAttribute in piecesList:
        classAttribute.widget.config(bg=clickBoxColourList[(classAttribute.column + classAttribute.row) % 2])
    elif classAttribute.piece_contained == 1000:
        classAttribute.widget.config(bg=clickBoxColourList[(classAttribute.column + classAttribute.row) % 2])
    else:
        piecesList[classAttribute.piece_contained].widget.config(
            bg=clickBoxColourList[(classAttribute.column + classAttribute.row) % 2])


def widget_highlight_remover(classAttribute):
    if classAttribute in piecesList:
        classAttribute.widget.config(bg=boxColourList[(classAttribute.column + classAttribute.row) % 2])
    elif classAttribute.piece_contained == 1000:
        classAttribute.widget.config(bg=boxColourList[(classAttribute.column + classAttribute.row) % 2])
    else:
        piecesList[classAttribute.piece_contained].widget.config(
            bg=boxColourList[(classAttribute.column + classAttribute.row) % 2])


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
    return [[7,23], [23,7]][[0, 0, 1, 1][SIDE_OF_WHITE]][colour]

def which_side_move():
    global MOVES_PLAYED
    return (MOVES_PLAYED + 1 + SIDE_COLOUR_VAR) % 2

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
                       pieceCodeVar, bool(j), rookKnightBishopcolumn[0][columnLoop], 7 * j, bool(1), int(0)))
            piece_creator_function(pieceCodeVar, j)
            typeCodeVar += 1
            pieceCodeVar += 1

            piecesList.append(
                Pieces(Label(gameWindow),
                       typeCodeVar,
                       pieceCodeVar, bool(j), rookKnightBishopcolumn[1][columnLoop], 7 * j, bool(1), int(0)))
            piece_creator_function(pieceCodeVar, j)
            typeCodeVar += 1
            pieceCodeVar += 1

            piecesList.append(
                Pieces(Label(gameWindow),
                       typeCodeVar,
                       pieceCodeVar, bool(j), rookKnightBishopcolumn[2][columnLoop], 7 * j, bool(1), int(0)))
            piece_creator_function(pieceCodeVar, j)
            typeCodeVar += 1
            pieceCodeVar += 1

        piecesList.append(
            Pieces(Label(gameWindow), typeCodeVar,
                   pieceCodeVar, bool(j), 3, 7 * j, bool(1), int(0)))
        piece_creator_function(pieceCodeVar, j)
        typeCodeVar += 1
        pieceCodeVar += 1

        piecesList.append(
            King(Label(gameWindow), typeCodeVar,
                 pieceCodeVar, bool(j), 4, 7 * j, bool(1), int(0)))
        piece_creator_function(pieceCodeVar, j)
        typeCodeVar += 1
        pieceCodeVar += 1

        for v in range(8):
            piecesList.append(
                Pieces(Label(gameWindow), typeCodeVar, pieceCodeVar, bool(j), v, 1 + 5 * j, bool(1), int(0)))
            piece_creator_function(pieceCodeVar, j)
            pieceCodeVar += 1
        typeCodeVar += 1
    for piece in piecesList:
        piece.widget.bind("<Button-1>", piece.clickFunc)
        piece.widget.bind("<Enter>", piece.cursorHighlighter)
        piece.widget.bind("<Leave>", piece.cursorHighlightRemover)


piece_constructor()






def simple_possible_destination_giver(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT = ENTIRE_BOARD_MATRIX):
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
                    position = 8 * (column_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + (1 + i) * v[0]) + row_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + (
                            1 + i) * v[1]
                    if column_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + (1 + i) * v[0] in range(8) and row_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + (
                            1 + i) * v[1] in range(8) and box_index_to_board_matrix_element_converter(position,
                                                                                                      ENTIRE_BOARD_MATRIX_INPUT) == 1000:
                        possibleDestinations.append(position)
                    elif column_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + (1 + i) * v[0] in range(8) and row_of_piece(
                            pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + (1 + i) * v[1] in range(
                        8) and box_index_to_board_matrix_element_converter(position,
                                                                           ENTIRE_BOARD_MATRIX_INPUT) not in like_coloured_piececode_list_spitter(
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
                    positionList = [[column_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + a, row_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + b],
                                    [column_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + b, row_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + a]]
                    for position in positionList:
                        if position[0] in range(8) and position[1] in range(
                                8) and box_index_to_board_matrix_element_converter(
                            8 * position[0] + position[1]) not in like_coloured_piececode_list_spitter(
                            pieceCodeInput):
                            possibleDestinations.append(8 * position[0] + position[1])
        elif piecesList[pieceCodeInput].typeCode == 4:
            # king
            unitVectorList = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
            for v in unitVectorList:
                position = 8 * (column_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + v[0]) + row_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + v[1]
                if column_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + v[0] in range(8) and row_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT) + v[1] in range(
                        8) and box_index_to_board_matrix_element_converter(position,
                                                                           ENTIRE_BOARD_MATRIX_INPUT) not in like_coloured_piececode_list_spitter(
                    pieceCodeInput):
                    possibleDestinations.append(position)
        elif piecesList[pieceCodeInput].typeCode == 5:
            pawnDirectionList = [1, -1]
            pawnDirection = pawnDirectionList[piecesList[pieceCodeInput].colour]
            pawnLongitudnalCoordinate = [row_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT), column_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT)][
                HORIZONTAL_VERTICAL_ARRANGEMENT_VAR]
            pawnLateralCoordinate = [column_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT), row_of_piece(pieceCodeInput, ENTIRE_BOARD_MATRIX_INPUT)][
                HORIZONTAL_VERTICAL_ARRANGEMENT_VAR]

            position = pieceCodeToPositionConverterMainBoard(pieceCodeInput) + pawnDirection * [1, 8][
                HORIZONTAL_VERTICAL_ARRANGEMENT_VAR] * 2
            if piecesList[pieceCodeInput].movesPlayedByPiece == 0 and box_index_to_board_matrix_element_converter(
                    position, ENTIRE_BOARD_MATRIX_INPUT) == 1000 and box_index_to_board_matrix_element_converter(
                position - pawnDirection * [1, 8][HORIZONTAL_VERTICAL_ARRANGEMENT_VAR],
                ENTIRE_BOARD_MATRIX_INPUT) == 1000:
                possibleDestinations.append(position)
            position = pieceCodeToPositionConverterMainBoard(pieceCodeInput) + pawnDirection * [1, 8][
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

        # print(possibleDestinations)
        return possibleDestinations

def final_destination_giver(piece_code_input, INPUT_BOARD_MATRIX = ENTIRE_BOARD_MATRIX, INPUT_PIECES_ALIVE = PIECES_ALIVE, INPUT_MOVES_PLAYED = MOVES_PLAYED):
    TEMP_BOARD_MATRIX = deepcopy(INPUT_BOARD_MATRIX)
    TEMP_PIECES_ALIVE = deepcopy(INPUT_PIECES_ALIVE)

    def reset_temp_board():
        nonlocal TEMP_BOARD_MATRIX, TEMP_PIECES_ALIVE
        TEMP_BOARD_MATRIX = deepcopy(INPUT_BOARD_MATRIX)
        TEMP_PIECES_ALIVE = deepcopy(INPUT_PIECES_ALIVE)

    initially_allowed_boxes = simple_possible_destination_giver(piece_code_input, INPUT_BOARD_MATRIX).copy()
    output = simple_possible_destination_giver(piece_code_input, INPUT_BOARD_MATRIX)


    for destination in initially_allowed_boxes:

        TEMP_BOARD_MATRIX[column_of_piece(piece_code_input, TEMP_BOARD_MATRIX)][row_of_piece(piece_code_input, TEMP_BOARD_MATRIX)] = 1000

        if TEMP_BOARD_MATRIX[destination // 8][destination % 8] in TEMP_PIECES_ALIVE[int(not which_side_move())]:
            TEMP_PIECES_ALIVE[int(not which_side_move())].remove(TEMP_BOARD_MATRIX[destination // 8][destination % 8])
        TEMP_BOARD_MATRIX[destination // 8][destination % 8] = piece_code_input
        for opp_piece in TEMP_PIECES_ALIVE[int(not which_side_move())]:
            if piececode_to_board_matrix_index_converter(king_code(which_side_move()), TEMP_BOARD_MATRIX) in simple_possible_destination_giver(opp_piece,TEMP_BOARD_MATRIX):

                output.remove(destination)
        reset_temp_board()

    return output


def computer_move_spitter():
    MOVES_PLAYED_ = MOVES_PLAYED
    ENTIRE_BOARD_MATRIX_ = ENTIRE_BOARD_MATRIX
    COMPUTER_PLAYER_POINTS_LIST_ = [SIDE_POINTS[computer_side_indicator_()],
                                    SIDE_POINTS[not (computer_side_indicator_())]]
    PEICES_ALIVE_ = PIECES_ALIVE

    def computer_side_indicator_():
        return (MOVES_PLAYED_ + 1 + SIDE_COLOUR_VAR) % 2

    COLUMNS_SLASH_ROWS_ = [[i.column for i in piecesList], [i.row for i in piecesList]]

    number_of_rounds_checked_ = 4
    move_options_matrix_ = [[], []]

    for i in range(number_of_rounds_checked_):
        for j in PIECES_ALIVE[MOVES_PLAYED_]:
            pass

    return [pieceCodeOutput, finalPosition]


def computer_piece_mover(computer_move_piece_code, final_position):
    global PIECE_CLICK_VAR
    PIECE_CLICK_VAR = computer_move_piece_code
    if boxesList[final_position].colour_occupied == 3:
        boxesList[final_position].pieceTeleporter('<Key>')
    else:
        piecesList[boxesList[final_position].piece_contained].clickFunc('<Key>')


# print("yeah")
# boxNumberer()
# print(ENTIRE_BOARD_MATRIX)
# print(PIECES_ALIVE)
gameWindow.mainloop()

'''
Make single player AI game which plays w itself for some rounds and chooses the best move to play w the human opponent

Also the capabilities of the AI game fully depend on the weights given to different pieces,
so make the next level of software to make these weights accurate using neural networks
'''

