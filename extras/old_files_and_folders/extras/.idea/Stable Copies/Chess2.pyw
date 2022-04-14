from tkinter import *

gameWindow = Tk()
gameWindow.title("Chess")
gameWindow.geometry('688x656')
gameWindow.resizable(0, 0)

PIECE_CLICK_VAR = 1000
MOVES_PLAYED = 0
LAST_MOVE = [[0, 0, 0]]
# [piececode, boxList index initial, boxList index final]

entireBoardMatrix = []
for r in range(8):
    entireBoardMatrix.append([])
    for c in range(8):
        entireBoardMatrix[r].append(1000)

piecesList = []
# list of all the piece instances of the class pieces (also subclass king)

boxesList = []
# list of all the box instances of the class boxes

pieceImageList = ['Piece images\\chessBlackRook.png', 'Piece images\\chessBlackKnight.png',
                  'Piece images\\chessBlackBishop.png',
                  'Piece images\\chessBlackQueen.png', 'Piece images\\chessBlackKing.png',
                  'Piece images\\chessBlackPawn.png', 'Piece images\\chessWhiteRook.png',
                  'Piece images\\chessWhiteKnight.png',
                  'Piece images\\chessWhiteBishop.png',
                  'Piece images\\chessWhiteQueen.png', 'Piece images\\chessWhiteKing.png',
                  'Piece images\\chessWhitePawn.png']
boxColourList = ['gold', 'darkred']
clickBoxColourList = ['khaki', 'darkmagenta']


class Boxes:
    def __init__(self, widget, column, row, colour, colour_occupied=3, piece_contained = 1000):
        self.widget = widget
        self.colour = bool(colour)
        self.column = int(column)
        self.row = int(row)
        self.colour_occupied = colour_occupied
        self.piece_contained = piece_contained
        # colour_occupied = 3 for not occupied, 0 for black and 1 for white

    def pieceTeleporter(self, event, victimCode=1000):
        global PIECE_CLICK_VAR, MOVES_PLAYED, LAST_MOVE
        if PIECE_CLICK_VAR < 1000 and boxesList.index(self) in simple_possible_destination_giver(
                PIECE_CLICK_VAR) and victimCode == 1000 or PIECE_CLICK_VAR < 1000 and pieceCodeToPositionConverter(
            victimCode) in simple_possible_destination_giver(PIECE_CLICK_VAR):
            for i in simple_possible_destination_giver(PIECE_CLICK_VAR):
                if i != boxesList.index(self):
                    widget_highlight_remover(boxesList[i])
            boxesList[LAST_MOVE[-1][1]].widget.config(bg=boxColourList[boxesList[LAST_MOVE[-1][1]].colour])
            piecesList[LAST_MOVE[-1][0]].widget.config(bg=boxColourList[boxesList[LAST_MOVE[-1][2]].colour])

            boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].colour_occupied = 3
            entireBoardMatrix[boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].column][
                boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].row] = 1000
            boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].piece_contained = 1000
            self.piece_contained = PIECE_CLICK_VAR
            boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].widget.config(
                bg=clickBoxColourList[(boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].colour)])
            LAST_MOVE.append([PIECE_CLICK_VAR, pieceCodeToPositionConverter(PIECE_CLICK_VAR),
                              8 * self.column + self.row])
            piecesList[PIECE_CLICK_VAR].column = self.column
            piecesList[PIECE_CLICK_VAR].row = self.row

            piecesList[PIECE_CLICK_VAR].widget.config(
                bg=clickBoxColourList[boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].colour])
            piecesList[PIECE_CLICK_VAR].widget.grid(row=self.row, column=self.column)
            piecesList[PIECE_CLICK_VAR].movesPlayedByPiece += 1
            self.colour_occupied = int(piecesList[PIECE_CLICK_VAR].colour)
            entireBoardMatrix[self.column][self.row] = piecesList[PIECE_CLICK_VAR].pieceCode

            PIECE_CLICK_VAR = 1000
            MOVES_PLAYED += 1


class Pieces:
    def __init__(self, widget, typeCode, pieceCode, colour, column, row, lifeState, movesPlayedByPiece,
                 clickState=bool(0),
                 art=None):
        self.art = art
        self.widget = widget
        self.typeCode = int(typeCode)
        self.colour = bool(colour)
        self.column = int(column)
        self.row = int(row)
        self.lifeState = lifeState
        self.movesPlayedByPiece = movesPlayedByPiece
        self.pieceCode = pieceCode
        self.clickState = clickState

    def cursorHighlighter(self, event = None):
        if (MOVES_PLAYED + 1) % 2 == self.colour and PIECE_CLICK_VAR == 1000:
            widget_highlighter(self)

    def cursorHighlightRemover(self, event = None):
        if (MOVES_PLAYED + 1) % 2 == self.colour and PIECE_CLICK_VAR == 1000:
            widget_highlight_remover(self)

    def clickFunc(self, event):
        global PIECE_CLICK_VAR, MOVES_PLAYED
        if (MOVES_PLAYED + 1) % 2 == self.colour:

            if PIECE_CLICK_VAR == 1000:
                PIECE_CLICK_VAR = self.pieceCode
                self.widget.config(
                    bg=clickBoxColourList[(piecesList[PIECE_CLICK_VAR].column + piecesList[PIECE_CLICK_VAR].row) % 2])
                simple_possible_destination_giver(PIECE_CLICK_VAR)
                for i in simple_possible_destination_giver(PIECE_CLICK_VAR):
                    widget_highlighter(boxesList[i])

            elif PIECE_CLICK_VAR == self.pieceCode:
                self.widget.config(bg=boxColourList[boxesList[
                    pieceCodeToPositionConverter(PIECE_CLICK_VAR)].colour])
                boxesList[8 * self.column + self.row].widget.config(bg=boxColourList[boxesList[
                    pieceCodeToPositionConverter(PIECE_CLICK_VAR)].colour])
                for i in simple_possible_destination_giver(PIECE_CLICK_VAR):
                    widget_highlight_remover(boxesList[i])
                PIECE_CLICK_VAR = 1000
            else:
                piecesList[PIECE_CLICK_VAR].widget.config(bg=boxColourList[boxesList[
                    pieceCodeToPositionConverter(PIECE_CLICK_VAR)].colour])
                boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].widget.config(
                    bg=boxColourList[(piecesList[PIECE_CLICK_VAR].column + piecesList[PIECE_CLICK_VAR].row) % 2])
                for i in simple_possible_destination_giver(PIECE_CLICK_VAR):
                    widget_highlight_remover(boxesList[i])
                PIECE_CLICK_VAR = self.pieceCode
                self.widget.config(
                    bg=clickBoxColourList[(piecesList[PIECE_CLICK_VAR].column + piecesList[PIECE_CLICK_VAR].row) % 2])
                boxesList[8 * self.column + self.row].widget.config(
                    bg=clickBoxColourList[(piecesList[PIECE_CLICK_VAR].column + piecesList[PIECE_CLICK_VAR].row) % 2])
                simple_possible_destination_giver(PIECE_CLICK_VAR)
                for i in simple_possible_destination_giver(PIECE_CLICK_VAR):
                    widget_highlighter(boxesList[i])
        elif PIECE_CLICK_VAR < 1000:
            self.widget.grid_remove()
            boxesList[pieceCodeToPositionConverter(self.pieceCode)].pieceTeleporter(event, self.pieceCode)


class King(Pieces):
    def __init__(self, widget, typeCode, pieceCode, colour, column, row, lifeState, movesPlayedByPiece,
                 clickState=bool(0),
                 art=None, checkState=bool(0)):
        super().__init__(widget, typeCode, pieceCode, colour, column, row, lifeState, movesPlayedByPiece, art)
        self.checkState = checkState


#
#
# random use functions

def pieceImageBgColourGridPlacer(pieceCodeInput):
    # gives pieces their icon, bg colour, and places them in grid
    piecesList[pieceCodeInput].art = PhotoImage(
        file=pieceImageList[piecesList[pieceCodeInput].typeCode + piecesList[pieceCodeInput].colour * 6])
    piecesList[pieceCodeInput].widget.config(image=piecesList[pieceCodeInput].art,
                                             bg=boxColourList[
                                                 boxesList[pieceCodeToPositionConverter(pieceCodeInput)].colour],
                                             width=82, height=78)
    piecesList[pieceCodeInput].widget.grid(column=piecesList[pieceCodeInput].column,
                                           row=piecesList[pieceCodeInput].row)
    entireBoardMatrix[piecesList[pieceCodeInput].column][piecesList[pieceCodeInput].row] = pieceCodeInput
    boxesList[pieceCodeToPositionConverter(pieceCodeInput)].colour_occupied = int(piecesList[pieceCodeInput].colour)
    boxesList[pieceCodeToPositionConverter(pieceCodeInput)].piece_contained = pieceCodeInput


def pieceCodeToPositionConverter(pieceCodeInput):
    if pieceCodeInput != 1000:
        return int(8 * piecesList[pieceCodeInput].column + piecesList[pieceCodeInput].row)


def pieceLabelDefaultBGColourGiver(pieceCodeInput):
    pieceCodeInput[pieceCodeInput].widget.config(
        bg=boxColourList[boxesList[pieceCodeToPositionConverter(pieceCodeInput)].colour])

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


def pieceConstructor():
    pieceCodeVar = 0
    # for pieceCode
    typeCodeVar = 0
    # for typeCode
    # typeCodeVar is mostly used only for giving piece images
    for j in range(2):
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
            pieceImageBgColourGridPlacer(pieceCodeVar)
            typeCodeVar += 1
            pieceCodeVar += 1

            piecesList.append(
                Pieces(Label(gameWindow),
                       typeCodeVar,
                       pieceCodeVar, bool(j), rookKnightBishopcolumn[1][columnLoop], 7 * j, bool(1), int(0)))
            pieceImageBgColourGridPlacer(pieceCodeVar)
            typeCodeVar += 1
            pieceCodeVar += 1

            piecesList.append(
                Pieces(Label(gameWindow),
                       typeCodeVar,
                       pieceCodeVar, bool(j), rookKnightBishopcolumn[2][columnLoop], 7 * j, bool(1), int(0)))
            pieceImageBgColourGridPlacer(pieceCodeVar)
            typeCodeVar += 1
            pieceCodeVar += 1

        piecesList.append(
            Pieces(Label(gameWindow), typeCodeVar,
                   pieceCodeVar, bool(j), 3, 7 * j, bool(1), int(0)))
        pieceImageBgColourGridPlacer(pieceCodeVar)
        typeCodeVar += 1
        pieceCodeVar += 1

        piecesList.append(
            King(Label(gameWindow), typeCodeVar,
                 pieceCodeVar, bool(j), 4, 7 * j, bool(1), int(0)))
        pieceImageBgColourGridPlacer(pieceCodeVar)
        typeCodeVar += 1
        pieceCodeVar += 1

        for v in range(8):
            piecesList.append(
                Pieces(Label(gameWindow), typeCodeVar, pieceCodeVar, bool(j), v, 1 + 5 * j, bool(1), int(0)))
            pieceImageBgColourGridPlacer(pieceCodeVar)
            pieceCodeVar += 1
        typeCodeVar += 1
    for piece in piecesList:
        piece.widget.bind("<Button-1>", piece.clickFunc)
        piece.widget.bind("<Enter>", piece.cursorHighlighter)
        piece.widget.bind("<Leave>", piece.cursorHighlightRemover)


pieceConstructor()


def boxNumberer():
    for a in boxesList:
        a.widget.config(text="{}".format(boxesList.index(a)))


def simple_possible_destination_giver(pieceCodeInput):
    if PIECE_CLICK_VAR < 1000:
        possibleDestinations = []
        rookBishopQueenTypeCodeList = [0, 2, 3]
        if piecesList[pieceCodeInput].typeCode in rookBishopQueenTypeCodeList:
            unitVectorList = [[[0, 1], [0, -1], [1, 0], [-1, 0]], [[1, 1], [1, -1], [-1, 1], [-1, -1]],
                              [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]]
            for v in unitVectorList[rookBishopQueenTypeCodeList.index(piecesList[pieceCodeInput].typeCode)]:
                for i in range(7):
                    position = 8 * (piecesList[pieceCodeInput].column + (1 + i) * v[0]) + piecesList[
                        pieceCodeInput].row + (1 + i) * v[1]
                    if piecesList[pieceCodeInput].column + (1 + i) * v[0] in range(8) and piecesList[
                        pieceCodeInput].row + (
                            1 + i) * v[1] in range(8) and boxesList[position].colour_occupied == 3:
                        possibleDestinations.append(position)
                    elif piecesList[pieceCodeInput].column + (1 + i) * v[0] in range(8) and piecesList[
                        pieceCodeInput].row + (
                            1 + i) * v[1] in range(8) and boxesList[position].colour_occupied != int(
                        piecesList[pieceCodeInput].colour):
                        possibleDestinations.append(position)
                        break
                    else:
                        break
        elif piecesList[pieceCodeInput].typeCode == 1:
            positionCheckerIndexList = [[1, -1], [2, -2]]
            for a in positionCheckerIndexList[0]:
                for b in positionCheckerIndexList[1]:
                    positionList = [[piecesList[pieceCodeInput].column + a, piecesList[pieceCodeInput].row + b],
                                    [piecesList[pieceCodeInput].column + b, piecesList[pieceCodeInput].row + a]]
                    for position in positionList:
                        if position[0] in range(8) and position[1] in range(8) and boxesList[
                            8 * position[0] + position[1]].colour_occupied != piecesList[pieceCodeInput].colour:
                            possibleDestinations.append(8 * position[0] + position[1])
        elif piecesList[pieceCodeInput].typeCode == 4:
            unitVectorList = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
            for v in unitVectorList:
                position = 8 * (piecesList[pieceCodeInput].column + v[0]) + piecesList[pieceCodeInput].row + v[1]
                if piecesList[pieceCodeInput].column + v[0] in range(8) and piecesList[pieceCodeInput].row + v[
                    1] in range(8) and boxesList[position].colour_occupied == 3:
                    possibleDestinations.append(position)
                elif piecesList[pieceCodeInput].column + v[0] in range(8) and piecesList[pieceCodeInput].row + v[
                    1] in range(8) and boxesList[position].colour_occupied != int(piecesList[pieceCodeInput].colour):
                    possibleDestinations.append(position)
                    break
                else:
                    break
        elif piecesList[pieceCodeInput].typeCode == 5:
            pawnDirectionList = [1, -1]
            pawnDirection = pawnDirectionList[piecesList[pieceCodeInput].colour]
            position = pieceCodeToPositionConverter(pieceCodeInput) + pawnDirection * 2
            if piecesList[pieceCodeInput].movesPlayedByPiece == 0 and boxesList[position].colour_occupied == 3 and \
                    boxesList[position - pawnDirection].colour_occupied == 3:
                possibleDestinations.append(position)
            position = pieceCodeToPositionConverter(pieceCodeInput) + pawnDirection
            if boxesList[position].colour_occupied == 3 and piecesList[pieceCodeInput].row + pawnDirection * 1 in range(
                    8):
                possibleDestinations.append(position)

            pawnColumnMovementList = [1, -1]
            for n in pawnColumnMovementList:
                position = 8 * (piecesList[pieceCodeInput].column + n) + (
                        piecesList[pieceCodeInput].row + pawnDirection)
                if piecesList[pieceCodeInput].row + pawnDirection in range(8) and piecesList[
                    pieceCodeInput].column + n in range(8) and boxesList[position].colour_occupied not in [3,
                                                                                                           int(
                                                                                                               piecesList[
                                                                                                                   pieceCodeInput].colour)]:
                    possibleDestinations.append(position)

        # print(possibleDestinations)
        return possibleDestinations



# print("yeah")
# boxNumberer()
gameWindow.mainloop()

'''
Make single player AI game which plays w itself for some rounds and chooses the best move to play w the human opponent

Also the capabilities of the AI game fully depend on the weights given to different pieces,
so make the next level of software to make these weights accurate using neural networks
'''
