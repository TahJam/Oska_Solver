"""
This file contains the functions necessary to generate all possible moves from a given Oska board.
Top function: moveGen(board, curr_player) -> List[List[str]]:
    will have two parameters: a list of strings representing the board and a char representing who's turn it is
    Does not do any error checking, assumes all input is valid input
    returns a list of all possible moves
"""
from typing import List
from copy import deepcopy

"""
Top function for generating new moves given a board and which curr_player's turn it is

@:param board: a list of strings representing the board
@:param curr_player: a char value of either 'b' or 'w' which represents who's turn it is
@:return a list of lists of strings which is all the possible moves that can be generated for the current curr_player
"""


def moveGen(initialBoard: List[str], piece: str) -> List[List[str]]:
    new = []
    # convert the board to 2d list of chars
    board = initialBoard
    # go through the board and find all the pieces for the curr_player
    for idx, row in enumerate(board):
        for jdx, cell in enumerate(row):
            if cell == piece:
                playerPiece = Piece(cell, idx, jdx)
                # generate the moves for the curr_player's piece
                moves = possibleMoves(board, playerPiece)
                # append all the new moves generated
                for move in moves:
                    new.append(move)
    return new


"""
Object for a piece
Keeps track of which curr_player the piece belongs to and its current position on the board
"""


class Piece:
    def __init__(self, player: str, i: int, j: int):
        self.player = player
        self.row = i
        self.col = j

    # function to just print out the object. Used for debugging purposes
    def __str__(self):
        return f'{self.player=}, {self.row=}, {self.col=}'


"""
Function to generate the moves for an individual piece on the board
@:param board: the current board 
@:param playerPiece: the current piece that will be used to generate the new moves for
@:return a list of list of str that will represent all the possible moves this current playerPiece can make
"""


def possibleMoves(board: List[List[str]], playerPiece: Piece) -> List[List[List[str]]]:
    # depending on which curr_player it is, the moves will either be going downwards or upwards.
    # so depending on whose turn it is, return the appropriate moves
    if playerPiece.player == 'w':
        return whiteMoves(board, playerPiece)
    else:
        # the black moves
        return blackMoves(board, playerPiece)


"""
Function to generate the moves of a given white piece on the board. Does not do any error checking, assumes all input is 
valid.
@:param board: the current board
@:param playerPiece: the piece that will be moved
@:return a list of list of str that will represent all the possible moves this current white playerPiece can make
"""


def whiteMoves(board: List[List[str]], playerPiece: Piece) -> List[List[List[str]]]:
    moves = []
    # need the row and col of the current piece to determine which moves can be made from this position
    row, col = playerPiece.row, playerPiece.col
    # need the size of the board to know the bounds of the board
    size = len(board)

    # if the col is 0, then can't go diagonally to the left cause out of bounds unless its on the lower half of the
    # board
    if col == 0:
        # Moving forward
        # two scenarios: piece is either on the upper half or on the lower half
        if row < size - 1 and board[row + 1][col] == '-':
            moves.append(forward(board, playerPiece, row + 1, col))
        # lower half
        if (size - 1) // 2 <= row < size - 1 and board[row + 1][col + 1] == '-':
            moves.append(forward(board, playerPiece, row + 1, col + 1))

        # if there is an opponent's piece then capture
        # upper half
        if row < size - 2 and row != ((size - 1) // 2) - 1 and board[row + 1][col] == 'b' and board[row + 2][
            col] == '-':
            oppPiece = Piece('b', row + 1, col)
            moves.append(capture(board, playerPiece, oppPiece, row + 2, col))
        # the piece is on the row just above the center
        if row == ((size - 1) // 2) - 1 and board[row + 1][col] == 'b' and board[row + 2][col + 1] == '-':
            oppPiece = Piece('b', row + 1, col)
            moves.append(capture(board, playerPiece, oppPiece, row + 1, col + 1))
        # if the piece is on the lower half of the board
        if (size - 1) // 2 <= row < size - 2 and board[row + 1][col + 1] == 'b' and board[row + 2][col + 2] == '-':
            oppPiece = Piece('b', row + 1, col + 1)
            moves.append(capture(board, playerPiece, oppPiece, row + 2, col + 2))
    # the piece is on the far right most side of the current row
    elif col == len(board[row]) - 1:
        # same thing again, generate the forward moves then the capture moves
        # forward moves - upper half
        if row < (size - 1) // 2 and board[row + 1][col - 1] == '-':
            moves.append(forward(board, playerPiece, row + 1, col - 1))
        # forward moves - lower half
        if (size - 1) // 2 <= row < size - 1:
            if board[row + 1][col] == '-':
                moves.append(forward(board, playerPiece, row + 1, col))
            if board[row + 1][col + 1] == '-':
                moves.append(forward(board, playerPiece, row + 1, col + 1))

        # capture moves - upper half
        if row < ((size - 1) // 2) - 1 and board[row + 1][col - 1] == 'b' and board[row + 2][col - 2] == '-':
            oppPiece = Piece('b', row + 1, col - 1)
            moves.append(capture(board, playerPiece, oppPiece, row + 2, col - 2))
        # capture moves - row above the center row
        if row == ((size - 1) // 2) - 1 and board[row + 1][col - 1] == 'b' and board[row + 2][col - 1] == '-':
            oppPiece = Piece('b', row + 1, col - 1)
            moves.append(capture(board, playerPiece, oppPiece, row + 2, col - 1))
        # capture moves - lower half
        if (size - 1) // 2 <= row < size - 2:
            # capture moves - right side lower half
            if board[row + 1][col + 1] == 'b' and board[row + 2][col + 2]:
                oppPiece = Piece('b', row + 1, col + 1)
                moves.append(capture(board, playerPiece, oppPiece, row + 2, col + 2))
            # capture moves - left side lower half
            if board[row + 1][col] == 'b' and board[row + 2][col] == '-':
                oppPiece = Piece('b', row + 1, col)
                moves.append(capture(board, playerPiece, oppPiece, row + 2, col))
    # piece is in the middle of the row
    else:
        # upper half forward and capture moves
        if row < (size - 1) // 2:
            # upper half left forward and capture moves
            # forward move - left
            if board[row + 1][col - 1] == '-':
                moves.append(forward(board, playerPiece, row + 1, col - 1))
            # capture move - left
            if col > 1 and board[row + 1][col - 1] == 'b' and board[row + 2][col - 2] == '-':
                oppPiece = Piece('b', row + 1, col - 1)
                moves.append(capture(board, playerPiece, oppPiece, row + 2, col - 2))
            # piece is on the row above center
            if col == 1 and row == ((size - 1) // 2) - 1 and board[row + 1][col - 1] == 'b' and board[row + 2][
                col - 1] == '-':
                oppPiece = Piece('b', row + 1, col - 1)
                moves.append(capture(board, playerPiece, oppPiece, row + 2, col - 1))

            # upper half right forward and capture moves
            # forward move - right
            if board[row + 1][col] == '-':
                moves.append(forward(board, playerPiece, row + 1, col))
            # capture move - right
            if len(board[row + 2]) > col and row != ((size - 1) // 2) - 1 and board[row + 1][col] == 'b' and \
                    board[row + 2][col] == '-':
                oppPiece = Piece('b', row + 1, col)
                moves.append(capture(board, playerPiece, oppPiece, row + 2, col))
            # piece is on the row just above the center
            if len(board[row + 2]) > col + 1 and row == ((size - 1) // 2) - 1 and board[row + 1][col] == 'b' and \
                    board[row + 2][
                        col + 1] == '-':
                oppPiece = Piece('b', row + 1, col)
                moves.append(capture(board, playerPiece, oppPiece, row + 2, col + 1))
        # lower half forward and capture moves
        else:
            # forward move - left
            if row < size - 1 and board[row + 1][col] == '-':
                moves.append(forward(board, playerPiece, row + 1, col))
            # capture move - left
            if row < size - 2 and board[row + 1][col] == 'b' and board[row + 2][col] == '-':
                oppPiece = Piece('b', row + 1, col)
                moves.append(capture(board, playerPiece, oppPiece, row + 2, col))

            # forward move - right
            if row < size - 1 and board[row + 1][col + 1] == '-':
                moves.append(forward(board, playerPiece, row + 1, col + 1))
            # capture move - right
            if row < size - 2 and board[row + 1][col + 1] == 'b' and board[row + 2][col + 2] == '-':
                oppPiece = Piece('b', row + 1, col + 1)
                moves.append(capture(board, playerPiece, oppPiece, row + 2, col + 2))

    return moves


"""
Function to generate the moves of a given black piece on the board. Does not do any error checking, assumes all input is 
valid.
@:param board: the current board
@:param playerPiece: the piece that will be moved
@:return a list of list of str that will represent all the possible moves this current black playerPiece can make
"""


def blackMoves(board: List[List[str]], playerPiece: Piece) -> List[List[List[str]]]:
    # list that will contain all the generated moves
    moves = []
    # need the row and col of the current piece to determine which moves can be made from this position
    row, col = playerPiece.row, playerPiece.col
    # need the size of the board to know the bounds of the board
    size = len(board)

    # if the piece is on the far left of the curr row
    if col == 0:
        # forward moves - upper half
        if row <= (size - 1) // 2 and board[row - 1][col + 1] == '-':
            moves.append(forward(board, playerPiece, row - 1, col + 1))
        if row > 0 and board[row - 1][col] == '-':
            moves.append(forward(board, playerPiece, row - 1, col))

        # capture moves - upper half
        if 1 < row <= (size - 1) // 2 and board[row - 1][col + 1] == 'w' and board[row - 2][col + 2] == '-':
            oppPiece = Piece('w', row - 1, col + 1)
            moves.append(capture(board, playerPiece, oppPiece, row - 2, col + 2))
        # capture moves - lower half
        if row != ((size - 1) // 2) + 1 and row > 1 and board[row - 1][col] == 'w' and board[row - 2][col] == '-':
            oppPiece = Piece('w', row - 1, col)
            moves.append(capture(board, playerPiece, oppPiece, row - 2, col))
        # capture moves - row just below center row
        if row == ((size - 1) // 2) + 1 and board[row - 1][col] == 'w' and board[row - 2][col + 1] == '-':
            oppPiece = Piece('w', row - 1, col)
            moves.append(capture(board, playerPiece, oppPiece, row - 2, col + 1))

    elif col == len(board[row]) - 1:  # the curr piece is on the far right side of the curr row
        # forward moves - upper half
        if 1 <= row <= (size - 1) // 2:
            if board[row - 1][col + 1] == '-':
                moves.append(forward(board, playerPiece, row - 1, col + 1))
            if board[row - 1][col] == '-':
                moves.append(forward(board, playerPiece, row - 1, col))

        # forward moves - lower half
        if row > (size - 1) // 2 and board[row - 1][col - 1] == '-':
            moves.append(forward(board, playerPiece, row - 1, col - 1))

        # capture moves - upper half
        if 1 < row <= (size - 1) // 2:
            if board[row - 1][col + 1] == 'w' and board[row - 2][col + 2] == '-':
                oppPiece = Piece('w', row - 1, col + 1)
                moves.append(capture(board, playerPiece, oppPiece, row - 2, col + 2))
            if board[row - 1][col] == 'w' and board[row - 2][col] == '-':
                oppPiece = Piece('w', row - 1, col)
                moves.append(capture(board, playerPiece, oppPiece, row - 2, col))
        # capture moves - lower half
        if row > ((size - 1) // 2) + 1 and board[row - 1][col - 1] == 'w' and board[row - 2][col - 2] == '-':
            oppPiece = Piece('w', row - 1, col - 1)
            moves.append(capture(board, playerPiece, oppPiece, row - 2, col - 2))

        # capture moves - row just below the center
        if row == ((size - 1) // 2) + 1 and board[row - 1][col - 1] == 'w' and board[row - 2][col - 1] == '-':
            oppPiece = Piece('w', row - 1, col - 1)
            moves.append(capture(board, playerPiece, oppPiece, row - 2, col - 1))
    else:  # piece is in the middle of the row, so it can move in both directions
        # forward and capture moves - upper half
        if row < (size - 1) // 2:
            if row > 0 and board[row - 1][col] == '-':  # forward move - left
                moves.append(forward(board, playerPiece, row - 1, col))
            if row > 1 and board[row - 1][col] == 'w' and board[row - 2][col] == '-':  # capture move - left
                oppPiece = Piece('w', row - 1, col)
                moves.append(capture(board, playerPiece, oppPiece, row - 2, col))

            if row > 0 and board[row - 1][col + 1] == '-':  # forward move - right
                moves.append(forward(board, playerPiece, row - 1, col + 1))
            if row > 1 and board[row - 1][col + 1] == 'w' and board[row - 2][col + 2] == '-':  # capture move - right
                oppPiece = Piece('w', row - 1, col + 1)
                moves.append(capture(board, playerPiece, oppPiece, row - 2, col + 2))
        else:  # forward and capture moves - lower half
            if board[row - 1][col - 1] == '-':  # forward move - left
                moves.append(forward(board, playerPiece, row - 1, col - 1))
            if col > 1 and board[row - 1][col - 1] == 'w' and board[row - 2][col - 2] == '-':  # capture move - left
                oppPiece = Piece('w', row - 1, col - 1)
                moves.append(capture(board, playerPiece, oppPiece, row - 2, col - 2))
            # capture move - row just below the center row
            if col == 1 and row == ((size - 1) // 2) + 1 and board[row - 1][col - 1] == 'w' and board[row - 2][
                col - 1] == '-':
                oppPiece = Piece('w', row - 1, col - 1)
                moves.append(capture(board, playerPiece, oppPiece, row - 2, col - 1))

            # capture and forward moves - right
            if board[row - 1][col] == '-':
                moves.append(forward(board, playerPiece, row - 1, col))
            if col < len(board[row - 2]) and row != ((size - 1) // 2) + 1 and board[row - 1][col] == 'w' and \
                    board[row - 2][col] == '-':
                oppPiece = Piece('w', row - 1, col)
                moves.append(capture(board, playerPiece, oppPiece, row - 2, col))
            # capture move - row just below the center row
            if row == ((size - 1) // 2) + 1 and col + 1 < len(board[row - 2]) and board[row - 1][col] == 'w' and \
                    board[row - 2][col + 1] == '-':
                oppPiece = Piece('w', row - 1, col)
                moves.append(capture(board, playerPiece, oppPiece, row - 2, col + 1))

    return moves


"""
Function to make a forward move with no jumping over opponent's piece
@:param board: the current board
@:param playerPiece: the piece that will be moved
@ param newRow: the new row position for the playerPiece
@:param newCol: the new column position for the playerPiece
@:return a list of str which represents the updated board
"""


def forward(board: List[List[str]], playerPiece: Piece, newRow: int, newCol: int) -> List[List[str]]:
    new = deepcopy(board)
    row, col = playerPiece.row, playerPiece.col
    new[row][col] = '-'
    new[newRow][newCol] = playerPiece.player
    return new


"""
Function to make a forward move and capture an opponent's piece
@:param board: the current board
@:param playerPiece: the piece that will be moved
@:param oppPlayer: the piece that will be captured by the current curr_player
@ param newRow: the new row position for the playerPiece
@:param newCol: the new column position for the playerPiece
@:return a list of str which represents the updated board
"""


def capture(board: List[List[str]], playerPiece: Piece, oppPiece: Piece, newRow: int, newCol: int) -> List[List[str]]:
    new = deepcopy(board)
    rowPlayer, colPlayer = playerPiece.row, playerPiece.col
    rowOpp, colOpp = oppPiece.row, oppPiece.col

    new[rowPlayer][colPlayer] = '-'
    new[rowOpp][colOpp] = '-'

    new[newRow][newCol] = playerPiece.player
    return new
