"""
Function calls for playing one move on a valid given Oska board
It uses the moveGen function so that has been copied to this file (not imported)
The main function, oskaplayer(), is run and returns the next best move for whichever player the function was called
for.
"""

from copy import deepcopy
from typing import List

"""
Function definition for the main function. oskaplayer() will call other functions to return the next best move from a 
given Oska board. Function does not do any data validation on whether or not the board is a valid Oska board or whether 
the curr_player is a valid curr_player.

@:param initial_board: a List of strings that represent a valid Oska board 
@:param curr_player: a string representing the current curr_player (who's turn it is). Should only be 'w' or 'b'
@:param turn: an integer representing how many moves ahead the minmax function should look to determine the best move

@:return:
    a List of strings that represent the board after the next best move has been played
"""


def oskaplayer(initial_board: List[str], curr_player: str, depth: int) -> List[str]:
    # convert board into List[List[str]] for easier manipulation
    board = convert2D(initial_board)

    # use minmax function to determine the best move
    best = minmax(board, curr_player, depth)

    # check if minmax returned an actual board
    if best is None:
        return None
    else:
        # return best but convert it back to List[str] first
        return convertList(best)


"""
--------------------------------------------------Class definitions ---------------------------------------------------
Below are the classes used in this program
"""
"""
Class Player represents the pieces on the board and how many steps there are to the other side of the board
"""


class Player:
    def __init__(self, player: str, count: int, steps: int):
        self.player = player
        self.count = count
        self.steps = steps

    # overriding string function to print stuff out. Used for debugging purposes
    def __str__(self):
        return f'{self.player=}, {self.count=}, {self.steps=}'


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
Function for determining the next best move from a given board. It calls the turn first search function to determine 
what the best move is from the list of all possible moves returned by the movegen function. 

@:param board: a List[List[str]] that represents the current board
@:param curr_player: a str that represents the current curr_player
@:param turn: an integer representing how many moves ahead the dfs function should look to determine the best move

@:return:
    a List[List[str]] that represents the next best move from the board
"""


def minmax(board: List[List[str]], player: str, depth: int) -> List[List[str]]:
    # generate the next moves
    next_moves = moveGen(board, player)
    # if no new moves can be generated, then either a tie or opponent makes the next turn
    if not next_moves:
        temp = 'w' if player == 'b' else 'b'
        # meaning that the other curr_player can't play a move either, so it's a tie
        return None if not moveGen(board, temp) else board  # opponent can make a move so return the board
    else:
        howMany = 1  # to keep track of the current turn for the search
        # call the dfs function to get the index of the next best move from next_moves
        best_idx = dfs(board, player, player, howMany, depth)

        # return the best move
        return next_moves[best_idx]


"""
Depth first search function. Will search until the turn is reached by the function. It calls the evaluator function 
to determine which of the possible moves is the best one.

@:param board: the current board
@:param turn: the current curr_player for this current board. Who's turn it is
@:param player: the player that will be used to evaluate the best move for that player
@:param count: how deep the current search is
@:param turn: the max turn the function can go

@:return
    an integer value that represents the index of the best move
"""


def dfs(board: List[List[str]], turn: str, player: str, count: int, depth: int) -> int:
    # generate the new moves for the current board
    pos_moves = moveGen(board, turn)

    # base case 1: pos_moves is empty so evaluate the current board
    if not pos_moves:
        return evaluator(board, player)
    elif count == depth:  # base case 2: max turn has been reached, so evaluate all the boards
        goodness = [None for _ in range(len(pos_moves))]  # the goodness of the boards in the pos_moves
        for i, curr in enumerate(pos_moves):
            goodness[i] = evaluator(curr, player)
        # return the index of the best value (could be min or max value depending on whose turn it is
        return returnGoodness(goodness, depth, count)
    else:  # recursive steps
        # now it's the next curr_player's turn
        next_player = 'b' if turn == 'w' else 'w'
        goodness = [None for _ in range(len(pos_moves))]  # the goodness of the boards in pos_moves
        for i, curr in enumerate(pos_moves):
            good = dfs(curr, next_player, player, count + 1, depth)
            goodness[i] = good
        return returnGoodness(goodness, count, count)


"""
Function that evaluates the goodness of a given next potential board for the current curr_player. It first calculates the 
minimum number of steps for each curr_player to reach the other side of the board (a winning case). While doing this, 
it also calculates how many pieces each curr_player has left on the board. It uses the Player class to define objects that 
represent the curr_player and the opponent.
If there is a winning situation for curr_player:
    return +20
If there is a winning situation for opponent:
    return -20
If there is no winning or losing situation:
    return opp steps - curr_player steps

@:param possible_move: the next potential board
@:param curr_player: a char that represents the current curr_player

@:return:
    an integer value that represents the goodness of the board
"""


def evaluator(possible_move: List[List[str]], curr_player: str):
    # initialize values to be used in the Player objects
    white_count = white_steps = 0
    black_count = black_steps = 0

    # go through the board and count how many pieces and steps there are for both white and black
    for i, row in enumerate(possible_move):
        for j, cell in enumerate(row):
            if cell == 'w':
                white_steps += len(possible_move) - i - 1
                white_count += 1
            elif cell == 'b':
                black_steps += i
                black_count += 1
    # create the Player objects
    player = opponent = None
    if curr_player == 'w':
        player = Player('w', white_count, white_steps)
        opponent = Player('b', black_count, black_steps)
    elif curr_player == 'b':
        player = Player('b', black_count, black_steps)
        opponent = Player('w', white_count, white_steps)

    # evaluate the goodness of the move
    # if both players have their pieces on the other side
    if (player.steps == 0 and opponent.steps == 0) and (player.count != 0 and opponent.count != 0):
        # whichever has more pieces, wins
        if player.count > opponent.count:
            # print(f'{player.player=} and {player.player}count > {opponent.player}count: return 20')
            return 20
        elif opponent.count > player.count:
            # print(f'{player.player=} and {player.player}count < {opponent.player}count: return -20')
            return -20
    # player winning situation
    if opponent.count == 0 or player.steps == 0:
        # print(f'{player.player=} and {player.count=} or {opponent.count=}: return 20')
        return 20
    elif opponent.steps == 0 or player.count == 0:  # opponent winning situation
        # print(f'{player.player=} and {player.count=} or {opponent.count=}: return -20')
        return -20
    else:  # if there are no winning situation, return the difference in steps
        # print(f'{player.player=} and no winning or losing sit: return {opponent.steps-player.steps=}')
        return opponent.steps - player.steps


"""
Function that returns the index of the best move based on who's turn it is. Could be max or min of goodness list.

@:param goodness: a list of ints that represent the goodness value of the board. (the value in a key-value pair where 
                  the key is the board ex. goodness[0] is the good value of the board at pos_moves[0]).
@:param turn: an int that's used to determine whether to use the min function or the max function
@:param count: how deep the search has gone so far

@:return:
    an int value that represents the index of the best board in the pos_moves List (not passed to this function)
"""


def returnGoodness(goodness: List[int], turn: int, count: int):
    # get the index of the highest value in goodness
    if count == 1:
        max_good = goodness[0]
        output = 0
        for i, good in enumerate(goodness):
            if good > max_good:
                max_good = good
                output = i
        return output
    else:  # haven't reached root, so return evaluated value to parent
        # return max when it's curr_player turn and return min when its opp turn
        return max(goodness) if turn % 2 == 1 else min(goodness)


"""
Top function for generating new moves given a board and which curr_player's turn it is

@:param board: a list of strings representing the board
@:param curr_player: a char value of either 'b' or 'w' which represents who's turn it is
@:return a list of lists of strings which is all the possible moves that can be generated for the current curr_player
"""


def moveGen(board: List[List[str]], piece: str) -> List[List[List[str]]]:
    new = []
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
        if row < size - 2 and row != ((size - 1) // 2) - 1 and board[row + 1][col] == 'b' \
                and board[row + 2][col] == '-':
            oppPiece = Piece('b', row + 1, col)
            moves.append(capture(board, playerPiece, oppPiece, row + 2, col))
        # the piece is on the row just above the center
        if row == ((size - 1) // 2) - 1 and board[row + 1][col] == 'b' and board[row + 2][col + 1] == '-':
            oppPiece = Piece('b', row + 1, col)
            moves.append(capture(board, playerPiece, oppPiece, row + 2, col + 1))
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
            if board[row + 1][col + 1] == 'b' and board[row + 2][col + 2] == '-':
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


"""
Function to convert the initial input of the board to a 2D list of chars. This makes it easier to handle as strings 
are immutable in python
@:param initialBoard: a list of strings that represent the board
@:return a list of list of chars that represent the board
"""


def convert2D(initialBoard: List[str]) -> List[List[str]]:
    board = []
    for s in initialBoard:
        temp = []
        temp[:0] = s
        board.append(temp)
    return board


"""
Function to convert 2D to List[str]. 
@:param board: the List[List[str]] representation of the board
@:return a List[str] representation of the board
"""


def convertList(board: List[List[str]]) -> List[str]:
    temp = []
    for row in board:
        temp.append(''.join(row))
    return temp
