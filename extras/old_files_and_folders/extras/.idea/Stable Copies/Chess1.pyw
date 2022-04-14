from tkinter import *

gameWindow = Tk()
gameWindow.title("Chess")
gameWindow.geometry('688x656')
gameWindow.resizable(0, 0)

PIECE_CLICK_VAR = 69
MOVES_PLAYED = 0
LAST_MOVE = [[0, 0, 0]]
# [piececode, boxList index initial, boxList index final]

entireBoardMatrix = []
for r in range(8):
    entireBoardMatrix.append([])
    for c in range(8):
        entireBoardMatrix[r].append(69)

piecesList = []
# list of all the piece instances of the class pieces (also subclass king)

boxesList = []
# list of all the box instances of the class boxes

pieceColourList = ['white', 'black']
pieceImageList = ['Piece images\\chessWhiteRook.png', 'Piece images\\chessWhiteKnight.png',
                  'Piece images\\chessWhiteBishop.png',
                  'Piece images\\chessWhiteQueen.png', 'Piece images\\chessWhiteKing.png',
                  'Piece images\\chessWhitePawn.png',
                  'Piece images\\chessBlackRook.png', 'Piece images\\chessBlackKnight.png',
                  'Piece images\\chessBlackBishop.png',
                  'Piece images\\chessBlackQueen.png', 'Piece images\\chessBlackKing.png',
                  'Piece images\\chessBlackPawn.png']
boxColourList = ['darkred', 'gold']
clickBoxColourList = ['darkmagenta', 'khaki']


class Boxes:
    def __init__(self, widget, row, column, colour, occupied_status=3):
        self.widget = widget
        self.colour = bool(colour)
        self.row = int(row)
        self.column = int(column)
        self.occupied_status = occupied_status
        # occupied_status = 3 for not occupied, 0 for white and 1 for black

    def pieceTeleporter(self, event):
        global PIECE_CLICK_VAR, MOVES_PLAYED, LAST_MOVE
        if PIECE_CLICK_VAR < 69:
            boxesList[LAST_MOVE[-1][1]].widget.config(bg=boxColourList[boxesList[LAST_MOVE[-1][1]].colour])
            piecesList[LAST_MOVE[-1][0]].widget.config(bg=boxColourList[boxesList[LAST_MOVE[-1][2]].colour])

            boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].occupied_status = 3
            entireBoardMatrix[boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].row][
                boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].column] = 69
            boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].widget.config(
                bg=clickBoxColourList[(boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].colour)])
            LAST_MOVE.append([PIECE_CLICK_VAR, pieceCodeToPositionConverter(PIECE_CLICK_VAR),
                         8 * self.row + self.column])
            piecesList[PIECE_CLICK_VAR].row = self.row
            piecesList[PIECE_CLICK_VAR].column = self.column

            piecesList[PIECE_CLICK_VAR].widget.config(
                bg=clickBoxColourList[boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].colour])
            piecesList[PIECE_CLICK_VAR].widget.grid(column=self.column, row=self.row)
            piecesList[PIECE_CLICK_VAR].movesPlayedByPiece += 1
            self.occupied_status = int(piecesList[PIECE_CLICK_VAR].colour)
            entireBoardMatrix[self.row][self.column] = piecesList[PIECE_CLICK_VAR].pieceCode

            PIECE_CLICK_VAR = 69
            MOVES_PLAYED += 1
            print(entireBoardMatrix)
            print(LAST_MOVE)


class Pieces:
    def __init__(self, widget, typeCode, pieceCode, colour, row, column, lifeState, movesPlayedByPiece,
                 clickState=bool(0),
                 art=None):
        self.art = art
        self.widget = widget
        self.typeCode = int(typeCode)
        self.colour = bool(colour)
        self.row = int(row)
        self.column = int(column)
        self.lifeState = lifeState
        self.movesPlayedByPiece = movesPlayedByPiece
        self.pieceCode = pieceCode
        self.clickState = clickState

    def cursorHighlighter(self, event):
        if MOVES_PLAYED % 2 == self.colour and PIECE_CLICK_VAR == 69:
            self.widget.config(bg=clickBoxColourList[(self.row + self.column) % 2])

    def cursorHighlightRemover(self, event):
        if MOVES_PLAYED % 2 == self.colour and PIECE_CLICK_VAR == 69:
            self.widget.config(bg=boxColourList[(self.row + self.column) % 2])


    def clickFunc(self, event):
        global PIECE_CLICK_VAR, MOVES_PLAYED
        if MOVES_PLAYED % 2 == self.colour:

            if PIECE_CLICK_VAR == 69:
                PIECE_CLICK_VAR = self.pieceCode
                self.widget.config(
                    bg=clickBoxColourList[(piecesList[PIECE_CLICK_VAR].row + piecesList[PIECE_CLICK_VAR].column) % 2])

            elif PIECE_CLICK_VAR == self.pieceCode:
                self.widget.config(bg=boxColourList[boxesList[
                    pieceCodeToPositionConverter(PIECE_CLICK_VAR)].colour])
                boxesList[8 * self.row + self.column].widget.config(bg=boxColourList[boxesList[
                    pieceCodeToPositionConverter(PIECE_CLICK_VAR)].colour])
                PIECE_CLICK_VAR = 69
            else:
                piecesList[PIECE_CLICK_VAR].widget.config(bg=boxColourList[boxesList[
                    pieceCodeToPositionConverter(PIECE_CLICK_VAR)].colour])
                boxesList[pieceCodeToPositionConverter(PIECE_CLICK_VAR)].widget.config(
                    bg=boxColourList[(piecesList[PIECE_CLICK_VAR].row + piecesList[PIECE_CLICK_VAR].column) % 2])
                PIECE_CLICK_VAR = self.pieceCode
                self.widget.config(
                    bg=clickBoxColourList[(piecesList[PIECE_CLICK_VAR].row + piecesList[PIECE_CLICK_VAR].column) % 2])
                boxesList[8 * self.row + self.column].widget.config(
                    bg=clickBoxColourList[(piecesList[PIECE_CLICK_VAR].row + piecesList[PIECE_CLICK_VAR].column) % 2])
        elif PIECE_CLICK_VAR < 69:
            self.widget.grid_remove()
            boxesList[pieceCodeToPositionConverter(self.pieceCode)].pieceTeleporter(event)


class King(Pieces):
    def __init__(self, widget, typeCode, pieceCode, colour, row, column, lifeState, movesPlayedByPiece,
                 clickState=bool(0),
                 art=None, checkState=bool(0)):
        super().__init__(widget, typeCode, pieceCode, colour, row, column, lifeState, movesPlayedByPiece, art)
        self.checkState = checkState


#
#
# random use functions

def pieceImageBgColourGridPlacer(pieceCodeInput):
    # gives pieces their icon, bg colour, and places them in grid
    piecesList[pieceCodeInput].art = PhotoImage(file=pieceImageList[piecesList[pieceCodeInput].typeCode])
    piecesList[pieceCodeInput].widget.config(image=piecesList[pieceCodeInput].art,
                                             bg=boxColourList[
                                                 boxesList[pieceCodeToPositionConverter(pieceCodeInput)].colour],
                                             width=82, height=78)
    piecesList[pieceCodeInput].widget.grid(row=piecesList[pieceCodeInput].row,
                                           column=piecesList[pieceCodeInput].column)
    entireBoardMatrix[piecesList[pieceCodeInput].row][piecesList[pieceCodeInput].column] = pieceCodeInput
    boxesList[pieceCodeToPositionConverter(pieceCodeInput)].occupied_status = int(piecesList[pieceCodeInput].colour)


def pieceCodeToPositionConverter(pieceCodeInput):
    return int(8 * piecesList[pieceCodeInput].row + piecesList[pieceCodeInput].column)


def pieceLabelDefaultBGColourGiver(pieceCodeInput):
    pieceCodeInput[pieceCodeInput].widget.config(
        bg=boxColourList[boxesList[pieceCodeToPositionConverter(pieceCodeInput)].colour])


# random use functions end
#
#


def boardConstructor():
    for r in range(8):
        for c in range(8):
            boxesList.append(
                Boxes(Label(gameWindow, bg=boxColourList[(r + c) % 2], width=10, height=4), r, c,
                      (r + c) % 2))
            boxesList[8 * r + c].widget.grid(row=r, column=c)
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

        rookKnightBishopRow = [[0, 7], [1, 6], [2, 5]]

        for rowLoop in range(2):
            # for simple pieces
            if j == 0:
                typeCodeVar = 0
            else:
                typeCodeVar = 6

            piecesList.append(
                Pieces(Label(gameWindow),
                       typeCodeVar,
                       pieceCodeVar, bool(j), rookKnightBishopRow[0][rowLoop], 7 * j, bool(1), int(0)))
            pieceImageBgColourGridPlacer(pieceCodeVar)
            typeCodeVar += 1
            pieceCodeVar += 1

            piecesList.append(
                Pieces(Label(gameWindow),
                       typeCodeVar,
                       pieceCodeVar, bool(j), rookKnightBishopRow[1][rowLoop], 7 * j, bool(1), int(0)))
            pieceImageBgColourGridPlacer(pieceCodeVar)
            typeCodeVar += 1
            pieceCodeVar += 1

            piecesList.append(
                Pieces(Label(gameWindow),
                       typeCodeVar,
                       pieceCodeVar, bool(j), rookKnightBishopRow[2][rowLoop], 7 * j, bool(1), int(0)))
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

'''
def movementPermitter(r, c):
    # returns three dimensional matrix with 0s, 1s and 2s on xy lane and 32 peices on z axis (notAvailable, available, dead)
    pass


def boxHighlighter(coordinates):
    # on clicking a piece (takes in input from movementPermitter)
    pass


def pieceMover(ri, ci, rf, cf):
    pass
'''

print("yeah")
gameWindow.mainloop()

'''
Make single player AI game which plays w itself for some rounds and chooses the best move to play w the human opponent

Also the capabilities of the AI game fully depend on the weights given to different pieces,
so make the next level of software to make these weights accurate using neural networks
'''
