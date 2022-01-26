position_of_queen = [3, 3, 4, 4][SIDE_OF_WHITE]
        position_of_king = [4, 4, 3, 3][SIDE_OF_WHITE]
        piecesList.append(
            Pieces(Label(gameWindow), typeCodeVar,
                    pieceCodeVar, bool(j), position_of_queen, 7 * j, bool(1), int(0)))

        piece_creator_function(pieceCodeVar, j)
        typeCodeVar += 1
        pieceCodeVar += 1

        piecesList.append(
            King(Label(gameWindow), typeCodeVar,
                    pieceCodeVar, bool(j), position_of_king, 7 * j, bool(1), int(0)))
        piece_creator_function(pieceCodeVar, j)
        typeCodeVar += 1
        pieceCodeVar += 1