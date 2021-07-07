"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0

    for row in board:
        x_count = x_count + row.count(X)
        o_count = o_count + row.count(O)
    
    if (x_count == 0) and (o_count == 0): # initial state is X (board is all empty)
        return X
    elif x_count > o_count: # (after intial state x first move)
        return O
    elif x_count <= o_count: # O always follow up X
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board. i is row (0,1,2)j is column (0,1,2)
    """
    possible_move = set()

    for i , row in enumerate(board):
        for j , col in enumerate(row):
            if col == EMPTY:
                possible_action.add((i,j))

    return possible_move


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # action is location in cell that AI is choose
    # need to keep original board to trace back the computation

    next_board = copy.deepcopy(board)
    print(id(board),id(next_board)) # debug

    # Modify the board with the player turn value (X or O) in location of cell (action(i,j))
    # action 0 is i action 1 is j 
    try:
        next_board[action(0)][action(1)] = player(board)
    except Exception as e:
        print(e)

    return next_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check vertical
    # Save player state on the first row of each column


    # check horiontal
    # Save player state on the first column of the row then compare to the rest (len must be 3)
    # If not proceed to next row
    # use list.count the first element in the row
    # Assume that it 3x3 board only
    
    for row in board:
        if (row.count(row[0]) == 3) and (row[0] != EMPTY):
            win_side = row[0]
            return win_side


    # check diagonal


    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
