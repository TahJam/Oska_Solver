import copy


# This function determines the next possible move for the given player
#   @param:
#   board: the game-board in the form of a list of strings
#   player: either 'b' or 'w', indicating whose turn it is
#   moves_ahead: the number of steps to look ahead
#
#   returns the next best move in the form of a game-board
def oskaplayer(board, player, moves_ahead):
    # Convert the input board to a 2D array
    initial_board = []
    for i in range(0, len(board)):
        new_row = []
        for j in range(0, len(board[i])):
            new_row.append(board[i][j])
        initial_board.append(new_row)

    # Use the minimax search to obtain the next best move
    ans = minmax(initial_board, player, moves_ahead)

    # If the move determined by the search is none, it means that both players
    # have reached a tie and the player could not move ahead
    if ans == None:
        return None

    return convert_format(ans)


# This function employs the minimax search to find the next best move
#   @param:
#   board: the gameboard in the form of a list of strings
#   player: either 'b' or 'w', indicating whose turn it is
#   moves: the number of steps to look ahead
#
#   returns the next best move in the form of a gameboard
def minmax(board, player, moves):
    # count records the current number of steps that we have searched
    count = 1

    # Employes a depth-first search algorithm to carry out the search
    # and we obtained the index of the best move among all the possible moves
    best = dfs(board, player, count, moves, player)
    next_moves = movegen(board, player)

    # If there is not any move that the player can make
    if not next_moves:
        # If both players cannot make any moves, then the game has reached a tie
        if not movegen(board, 'w' if player == 'b' else 'b'):
            return None
        # Else we let the opponent player make the next move
        return board

    return next_moves[best]


# This function carrys out a depth-first search with minimax algorithm to
# determine the next best move
#   @param:
#   board: the gameboard in the form of a list of strings
#   player: either 'b' or 'w', indicating whose turn it is
#   count: the current number of steps that we have already looked through
#   moves: the total number of steps to look ahead
#   starting_player: the player whose favor we are in to evaluate the board
#
#   returns
#   (1): when we are still searching level by level, this function returns the
#        evaluator value returned by the child node to the parent node
#   (2): when we have finished searching and evaluating the entire search tree,
#        this function returns the index of the best move in the list of all
#        possible moves
def dfs(board, player, count, moves, starting_player):
    new_boards = movegen(board, player)

    # If we have reached the max depth to look ahead, we stop generating new
    # boards, we evaluate all the boards

    # If there is no further moves that can be made from the current board,
    # we evaluate the current board and return the value to the parent node
    if not new_boards:
        return board_evaluator(board, starting_player)

    # If we have reached the lowest level of the search tree (leaf nodes),
    # we stop generating new boards and evaluate all the leaf nodes (boards)
    if count == moves:
        values = []
        for new_board in new_boards:
            values.append(board_evaluator(new_board, starting_player))

        # If we have finished evaluating all the boards and need to return the
        # correct index of the next move
        if count == 1:
            max_value = values[0]
            result = 0
            for i in range(0, len(values)):
                if max_value < values[i]:
                    max_value = values[i]
                    result = i
            return result

        # Or if we still need to return an evaluated value to the parent node and
        # have not reached the root
        else:
            if not values:
                pass
            elif moves % 2 == 0:
                return min(values)
            else:
                return max(values)

    # We have not yet reached the max depth, we continue to go deeper by
    # generating new boards
    else:
        # Here we also need to alternate to the opponent player
        new_player = player
        if player == 'w':
            new_player = 'b'
        else:
            new_player = 'w'
        values = []
        for new_board in new_boards:
            cur_val = dfs(new_board, new_player, count + 1, moves, starting_player)
            values.append(cur_val)

        # If we have finished evaluating all the boards and need to return the
        # correct index of the next move
        if count == 1:
            max_value = values[0]
            result = 0
            for i in range(len(values)):
                if max_value < values[i]:
                    max_value = values[i]
                    result = i
            return result

        # Or if we still need to return an evaluated value to the parent node and
        # have not reached the root
        else:
            if not values:
                pass
            elif count % 2 == 0:
                return min(values)
            else:
                return max(values)


# This function evaluates a static board in relation to the given player
# Here, I calculate the minimum number of steps that each player needs
# to reach the starting positions of the opponent. I also count the number
# of remaining pieces that each player has on the board.
#   I use the count and steps to determine if there is a winning situation.
#   If there is a winning situation for the player in my favor, I return 20
#   or else I return -20 (the  winning situation for the opposing player)
#   If there is no winning situation, we use the opponent's number of steps
#   minus the player's number of steps since the lesser the step, the better.
#
#   @param:
#   board: the gameboard in the form of a list of strings
#   starting_player: the player whose favor we are in to evaluate the board
#
#   returns
#   (1): when we are still searching level by level, this function returns the
#        evaluator value returned by the child node to the parent node
#   (2): when we have finished searching and evaluating the entire search tree,
#        this function returns the index of the best move in the list of all
#        possible moves
def board_evaluator(board, starting_player):
    white_count = 0
    black_count = 0
    white_step = 0
    black_step = 0

    # Goes through the board to count the number of pieces and the number of
    # steps for each player
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == 'b':
                black_count += 1
                black_step += i
            if board[i][j] == 'w':
                white_step += len(board) - i - 1
                white_count += 1

    # If the player that in favor holds the white piece
    # print(f'{starting_player=}')
    if starting_player == 'w':
        # If both players have all their pieces in place, we compare the
        # number of pieces
        if ((black_step == 0 and white_step == 0) and
                (black_count != 0 and white_count != 0)):
            if white_count > black_count:
                # print(f'{white_count} > {black_count} return 20')
                return 20
            elif white_count < black_count:
                # print(f'{white_count} < {black_count} return -20')
                return -20

        if black_count == 0 or white_step == 0:
            # print(f'{black_count=} or {white_step=} return 20')
            return 20
        elif white_count == 0 or black_step == 0:
            # print(f'{white_count=} or {black_step=} return 20')
            return -20
        else:
            # print(f'no winning or losing: return {black_step - white_step=}')
            return black_step - white_step
    # If the player that in favor holds the black piece
    else:
        # If both players have all their pieces in place, we compare the
        # number of pieces
        if ((black_step == 0 and white_step == 0) and
                (black_count != 0 and white_count != 0)):
            if white_count > black_count:
                # print(f'{white_count} > {black_count} return -20')
                return -20
            elif white_count < black_count:
                # print(f'{white_count} < {black_count} return 20')
                return 20

        if white_count == 0 or black_step == 0:
            # print(f'{white_count=} or {black_step=} return 20')
            return 20
        elif black_count == 0 or white_step == 0:
            # print(f'{black_count=} or {white_step=} return -20')
            return -20
        else:
            # print(f'no winning or losing: return {white_step - black_step=}')
            return white_step - black_step


# This function converts the format of board from 2D array to a list of strings
#   @param:
#   board: the gameboard
#
#   returns a list of gameboards in the form of list of strings
def convert_format(board):
    result = []
    for row in board:
        new_row = ""
        for col in row:
            new_row += col
        result.append(new_row)
    return result


# This function gets the minimum number of a given list
#   @param:
#   list: the list of numbers
#
#   returns the minimum number of the list
def min(list):
    result = list[0]
    for num in list:
        if result > num:
            result = num
    return result


# This function gets the maximum number of a given list
#   @param:
#   list: the list of numbers
#
#   returns the maximum number of the list
def max(list):
    result = list[0]
    for num in list:
        if result < num:
            result = num
    return result


# This function generates all the possible moves that the input player can make
#   @param:
#   initial_board: the gameboard
#   player: either 'b' or 'w', indicating whose turn it is
#
#   returns a list of newly generated gameboards
def movegen(initial_board, player):
    new_boards = []

    # Nested for loop to find all the pieces of the player
    for i in range(0, len(initial_board)):
        for j in range(0, len(initial_board[i])):
            if initial_board[i][j] == player:
                result = move(initial_board, i, j)
                for board in result:
                    new_boards.append(board)
    return new_boards


# This function determines whether the player is white or black and returns the
# corresponding new boards
#   @param:
#   board: the gameboard
#   row: the row index of the piece that will be moved
#   col: the column index of the piece that will be moved
#
#   returns a list of newly generated gameboards
def move(board, row, col):
    if board[row][col] == 'w':
        return white_move(board, row, col)
    else:
        return black_move(board, row, col)


# This function generates all the new boards when the player holds white
#   @param:
#   board: the gameboard
#   row: the row index of the piece that will be moved
#   col: the column index of the piece that will be moved
#
#   returns a list of newly generated gameboards
def white_move(board, row, col):
    size = len(board)
    forwards = []

    # If the piece is on the first of that row
    if col == 0:
        # Move forward
        if row < size - 1 and board[row + 1][0] == '-':
            forwards.append(forward(board, row, col, row + 1, 0))
        # If the piece is in the lower half of the board
        if ((size - 1) / 2 <= row < size - 1
                and board[row + 1][col + 1] == '-'):
            forwards.append(forward(board, row, col, row + 1, col + 1))

        # Jump forward
        # If the piece is in the upper half of the board
        if (row < (size - 2) and row != (size - 1) / 2 - 1 and
                board[row + 1][0] == 'b' and
                board[row + 2][0] == '-'):
            forwards.append(jump(board, row, col, row + 1, 0, row + 2, 0))
        # If the piece is on the line right above the middle line
        if (row == (size - 1) / 2 - 1 and
                board[row + 1][0] == 'b' and
                board[row + 2][1] == '-'):
            forwards.append(jump(board, row, col, row + 1, 0, row + 2, 1))
        # If the piece is in the lower half of the board
        if (row >= (size - 1) / 2 and row < size - 2
                and board[row + 1][col + 1] == 'b' and board[row + 2][col + 2] == '-'):
            forwards.append(jump(board, row, col, row + 1, col + 1, row + 2, col + 2))

    # if the piece is on the last of that row
    elif col == len(board[row]) - 1:
        # Move forward
        # If the piece is in the upper half of the board
        if (row < (size - 1) / 2 and board[row + 1][col - 1] == '-'):
            forwards.append(forward(board, row, col, row + 1, col - 1))
        # If the piece is in the lower half of the board
        if (row >= (size - 1) / 2 and row < size - 1):
            if board[row + 1][col] == '-':
                forwards.append(forward(board, row, col, row + 1, col))
            if board[row + 1][col + 1] == '-':
                forwards.append(forward(board, row, col, row + 1, col + 1))

        # Jump forward
        # If the piece is in the upper half of the board
        if (row < (size - 1) / 2 - 1 and
                board[row + 1][col - 1] == 'b' and
                board[row + 2][col - 2] == '-'):
            forwards.append(jump(board, row, col, row + 1, col - 1, row + 2, col - 2))
        # If the piece is on the line right above the middle line
        if (row == (size - 1) / 2 - 1 and
                board[row + 1][col - 1] == 'b' and
                board[row + 2][col - 1] == '-'):
            forwards.append(jump(board, row, col, row + 1, col - 1, row + 2, col - 1))
        # If the piece is in the lower half of the board
        if (size - 1) / 2 <= row < size - 2:
            if board[row + 1][col + 1] == 'b' and board[row + 2][col + 2] == '-':
                forwards.append(jump(board, row, col, row + 1, col + 1, row + 2, col + 2))
            if board[row + 1][col] == 'b' and board[row + 2][col] == '-':
                forwards.append(jump(board, row, col, row + 1, col, row + 2, col))

    # If the piece is in the middle of that row, it can move forward in
    # two directions
    else:
        # If the piece is in the upper half of the board
        if row < (size - 1) / 2:
            # Move forward to the left
            if board[row + 1][col - 1] == '-':
                forwards.append(forward(board, row, col, row + 1, col - 1))
            # Jump to the left
            if col > 1 and board[row + 1][col - 1] == 'b' and board[row + 2][col - 2] == '-':
                forwards.append(jump(board, row, col, row + 1, col - 1, row + 2, col - 2))
            # If the piece is on the line right above the middle line
            if (col == 1 and row == ((size - 1) / 2 - 1)
                    and board[row + 1][col - 1] == 'b'
                    and board[row + 2][col - 1] == '-'):
                forwards.append(jump(board, row, col, row + 1, col - 1, row + 2, col - 1))

            # Move forward to the right
            if board[row + 1][col] == '-':
                forwards.append(forward(board, row, col, row + 1, col))
            # Jump to the right
            if (len(board[row + 2]) > col and row != ((size - 1) / 2 - 1) and
                    board[row + 1][col] == 'b' and board[row + 2][col] == '-'):
                forwards.append(jump(board, row, col, row + 1, col, row + 2, col))
            # If the piece is on the line right above the middle line
            if (len(board[row + 2]) > (col + 1) and row == ((size - 1) / 2 - 1)
                    and board[row + 1][col] == 'b'
                    and board[row + 2][col + 1] == '-'):
                forwards.append(jump(board, row, col, row + 1, col, row + 2, col + 1))

        # If the piece is in the lower half of the board
        else:
            # Move forward to the left
            if (row < size - 1 and board[row + 1][col] == '-'):
                forwards.append(forward(board, row, col, row + 1, col))
            # Jump to the left
            if (row < size - 2 and board[row + 1][col] == 'b' and board[row + 2][col] == '-'):
                forwards.append(jump(board, row, col, row + 1, col, row + 2, col))

            # Move forward to the right
            if (row < size - 1 and board[row + 1][col + 1] == '-'):
                forwards.append(forward(board, row, col, row + 1, col + 1))
            # Jump to the right
            if (row < size - 2 and
                    board[row + 1][col + 1] == 'b' and board[row + 2][col + 2] == '-'):
                forwards.append(jump(board, row, col, row + 1, col + 1, row + 2, col + 2))
    return forwards


# This function generates all the new boards when the player holds white
#   @param:
#   board: the gameboard
#   row: the row index of the piece that will be moved
#   col: the column index of the piece that will be moved
#
#   returns a list of newly generated gameboards
def black_move(board, row, col):
    size = len(board)
    forwards = []

    # if the piece is on the first of that row
    if col == 0:
        # Move forward
        # If the piece is in the upper half of the board
        if (row <= (size - 1) / 2 and board[row - 1][col + 1] == '-'):
            forwards.append(forward(board, row, col, row - 1, col + 1))

        if (row > 0 and board[row - 1][0] == '-'):
            forwards.append(forward(board, row, col, row - 1, 0))

        # Jump forward
        # If the piece is in the upper half of the board, it can jump right
        if (row <= (size - 1) / 2 and row > 1
                and board[row - 1][col + 1] == 'w' and board[row - 2][col + 2] == '-'):
            forwards.append(jump(board, row, col, row - 1, col + 1, row - 2, col + 2))
        # If the piece is not on the line below the middle and jumps left
        if (row != (size - 1) / 2 + 1 and row > 1 and
                board[row - 1][0] == 'w' and
                board[row - 2][0] == '-'):
            forwards.append(jump(board, row, col, row - 1, 0, row - 2, 0))
        # If the piece is on the line right below the middle line
        if (row == ((size - 1) / 2 + 1) and
                board[row - 1][0] == 'w' and
                board[row - 2][1] == '-'):
            forwards.append(jump(board, row, col, row - 1, 0, row - 2, 1))

    # if the piece is on the last of that row
    elif col == len(board[row]) - 1:
        # Move forward
        # If the piece is in the upper half of the board
        if row <= (size - 1) / 2 and row >= 1:
            if board[row - 1][col + 1] == '-':
                forwards.append(forward(board, row, col, row - 1, col + 1))
            if board[row - 1][col] == '-':
                forwards.append(forward(board, row, col, row - 1, col))
        # If the piece is in the lower half of the board
        if (row > (size - 1) / 2 and board[row - 1][col - 1] == '-'):
            forwards.append(forward(board, row, col, row - 1, col - 1))

        # Jump forward
        # If the piece is in the upper half of the board, it can jump left
        if (row <= (size - 1) / 2 and row > 1):
            if (board[row - 1][col + 1] == 'w' and board[row - 2][col + 2] == '-'):
                forwards.append(jump(board, row, col, row - 1, col + 1, row - 2, col + 2))
            if (board[row - 1][col] == 'w' and board[row - 2][col] == '-'):
                forwards.append(jump(board, row, col, row - 1, col, row - 2, col))
        # If the piece is in the lower half of the board
        if (row > ((size - 1) / 2 + 1)
                and board[row - 1][col - 1] == 'w'
                and board[row - 2][col - 2] == '-'):
            forwards.append(jump(board, row, col, row - 1, col - 1, row - 2, col - 2))
        # If the piece is on the line right below the middle line
        if (row == ((size - 1) / 2 + 1)
                and board[row - 1][col - 1] == 'w'
                and board[row - 2][col - 1] == '-'):
            forwards.append(jump(board, row, col, row - 1, col - 1, row - 2, col - 1))

    # If the piece is in the middle of that row, it can move forward in
    # two directions
    else:
        # If the piece is in the upper half of the board
        if row < (size - 1) / 2:
            # Move forward to the left
            if row > 0 and board[row - 1][col] == '-':
                forwards.append(forward(board, row, col, row - 1, col))
            # Jump to the left
            if (row > 1 and board[row - 1][col] == 'w' and board[row - 2][col] == '-'):
                forwards.append(jump(board, row, col, row - 1, col, row - 2, col))

            # Move forward to the right
            if row > 0 and board[row - 1][col + 1] == '-':
                forwards.append(forward(board, row, col, row - 1, col + 1))
            # Jump to the right
            if (row > 1 and
                    board[row - 1][col + 1] == 'w' and board[row - 2][col + 2] == '-'):
                forwards.append(jump(board, row, col, row - 1, col + 1, row - 2, col + 2))

        # If the piece is in the lower half of the board
        else:
            # Move forward to the left
            if board[row - 1][col - 1] == '-':
                forwards.append(forward(board, row, col, row - 1, col - 1))
            # Jump to the left
            if (col > 1 and board[row - 1][col - 1] == 'w' and board[row - 2][col - 2] == '-'):
                forwards.append(jump(board, row, col, row - 1, col - 1, row - 2, col - 2))
            # If the piece is on the line right below the middle line
            if (col == 1 and row == ((size - 1) / 2 + 1)
                    and board[row - 1][col - 1] == 'w'
                    and board[row - 2][col - 1] == '-'):
                forwards.append(jump(board, row, col, row - 1, col - 1, row - 2, col - 1))

            # Move forward to the right
            if board[row - 1][col] == '-':
                forwards.append(forward(board, row, col, row - 1, col))
            # Jump to the right
            if (len(board[row - 2]) > col and row != ((size - 1) / 2 + 1) and
                    board[row - 1][col] == 'w' and board[row - 2][col] == '-'):
                forwards.append(jump(board, row, col, row - 1, col, row - 2, col))
            # If the piece is on the line right below the middle line
            if (row == ((size - 1) / 2 + 1) and len(board[row - 2]) > (col + 1)
                    and board[row - 1][col] == 'w'
                    and board[row - 2][col + 1] == '-'):
                forwards.append(jump(board, row, col, row - 1, col, row - 2, col + 1))
    return forwards


# This function moves the piece from the old position to the new position
#   @param:
#   board: the gameboard
#   old_row: the row index of the piece that will be moved
#   old_col: the column index of the piece that will be moved
#   new_row: the row index of the place that the piece will be moved to
#   new_col: the column index of the place that the piece will be moved to
#
#   returns the new gameboard
def forward(board, old_row, old_col, new_row, new_col):
    result = copy.deepcopy(board)
    result[old_row][old_col] = '-'
    result[new_row][new_col] = board[old_row][old_col]
    return result


# This function moves the piece from the old position to the new position,
# jumping over the opponent's piece in the middle
#   @param:
#   board: the gameboard
#   old_row: the row index of the piece that will be moved
#   old_col: the column index of the piece that will be moved
#   middle_row: the row index of the piece that will be removed by this jump
#   middle_col: the column index of the piece that will be removed by this jump
#   new_row: the row index of the place that the piece will be moved to
#   new_col: the column index of the place that the piece will be moved to
#
#   returns the new gameboard
def jump(board, old_row, old_col, middle_row, middle_col, new_row, new_col):
    result = copy.deepcopy(board)
    result[old_row][old_col] = '-'
    result[middle_row][middle_col] = '-'
    result[new_row][new_col] = board[old_row][old_col]
    return result

# Below is the code that I used to test the winning rate of the oskaplayer
# with my current heuristics, depending on the value of the number of steps
# to look ahead, the winning rate that I obtained is 90% in the range
# of [0.85, 0.95].
#
# from oskaplayer import oskaplayer
# from oskaplayer import convert_format
# from movegen import movegen
# import random
#
#
# # This function test the winning rate of the oskaplayer agains a random_player
# # Here, we only tested with three board examples with 100 test cases.
# #   @param:
# #
# #   returns:
# #           1 if the black wins
# #           2 if the white wins
# #           -1 f there is a tie
# def mass_game():
#     board4 = ['wwww','---','--','---','bbbb'];
#     board5 = ['wwwww','----','---','--','---','----','bbbbb'];
#     board6 = ['wwwwww','-----','----','---','--','---','----','-----','bbbbbb'];
#
#     total_game = 100
#
#     # board4
#     white_win_count = 0
#     i = 0
#
#     while i < total_game:
#         i += 1
#         result = game(board4)
#         if result == 2:
#             white_win_count += 1
#         elif result == -1:
#             i -= 1
#
#     print("BOARD4 white win rate = {}".format(white_win_count/total_game))
#
#     # board5
#     white_win_count = 0
#     i = 0
#
#     while i < total_game:
#         i += 1
#         result = game(board5)
#         if result == 2:
#             white_win_count += 1
#         elif result == -1:
#             i -= 1
#
#     print("BOARD5 white win rate = {}".format(white_win_count/total_game))
#
#     # board6
#     white_win_count = 0
#     i = 0
#
#     while i < total_game:
#         i += 1
#         result = game(board6)
#         if result == 2:
#             white_win_count += 1
#         elif result == -1:
#             i -= 1
#
#     print("BOARD6 white win rate = {}".format(white_win_count/total_game))
#
#
# # This function determines if there is a win for either player
# #   @param:
# #   board: the gameboard in the form of a list of strings
# #   player: either 'b' or 'w', indicating whose turn it is
# #
# #   returns:
# #           1 if the black wins
# #           2 if the white wins
# #           -1 f there is a tie
# def game(board):
#     player = 'w'
#     cur_board = board
#     while True:
#         if player == 'w':
#             # Here, I have tested with different values, including 1, 2, 3, 4...
#             cur_board = oskaplayer(cur_board, player, 2)
#             if cur_board is None:
#                 return -1
#             result = check_win(cur_board, player)
#             player = 'b'
#         else:
#             cur_board = random_player(cur_board)
#             result = check_win(cur_board, player)
#             player = 'w'
#
#         if result == 1:
#             return 1
#         if result == 2:
#             return 2
#
#
# # This function determines the next random move for the given player
# #   @param:
# #   board: the gameboard in the form of a list of strings
# #
# #   returns the next random move in the form of a gameboard
# def random_player(board):
#     initial_board = []
#     for i in range(0, len(board)):
#         new_row = []
#         for j in range(0, len(board[i])):
#             new_row.append(board[i][j])
#         initial_board.append(new_row)
#
#     new_boards = movegen(initial_board, 'b')
#     if new_boards == []:
#         return board
#     choice = int(random.random() * len(new_boards))
#     return convert_format(new_boards[choice])
#
#
# # This function determines if there is a win for either player
# #   @param:
# #   board: the gameboard in the form of a list of strings
# #   player: either 'b' or 'w', indicating whose turn it is
# #
# #   returns:
# #           1 if the black wins
# #           2 if the white wins
# #           0 if there is not winner currently
# def check_win(board, player):
#     white_count = 0
#     black_count = 0
#     white_step = 0
#     black_step = 0
#     for i in range(0, len(board)):
#         for j in range(0, len(board[i])):
#             if board[i][j] == 'b':
#                 black_count += 1
#                 black_step += i
#             if board[i][j] == 'w':
#                 white_step += len(board) - i - 1
#                 white_count += 1
#
#     if player == 'w':
#         if black_count == 0 or white_step == 0:
#             return 2
#         elif white_count == 0 or black_step == 0:
#             return 1
#     else:
#         if white_count == 0 or black_step == 0:
#             return 1
#         elif black_count == 0 or white_step == 0:
#             return 2
#     return 0
#
