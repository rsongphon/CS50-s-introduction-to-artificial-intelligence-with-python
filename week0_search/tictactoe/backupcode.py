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
                possible_move.add((i,j))

    return possible_move


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # action is location in cell that AI is choose
    # need to keep original board to trace back the computation

    next_board = copy.deepcopy(board)
    #print(id(board),id(next_board)) # debug

    # Modify the board with the player turn value (X or O) in location of cell (action(i,j))
    # action 0 is i action 1 is j 
    try:
        next_board[action[0]][action[1]] = player(board)
    except Exception as e:
        print('Error : ',e)

    return next_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
     # check function that recieve of array to check if all element is same
     # count the first element if the count is equal to number of element in array then all element are the same
     # also the first element must be player X or O not empty space
    def all_same(l):
        if (l.count(l[0]) == len(l)) and (l[0] != EMPTY):
            return True
        else:
            return False

    # check vertical
    # Save player state on the first row of each column

    # iterate 3 column , board[0] is first row >>> len(borad[0] is number of column)
    for col in range(len(board[0])):
        # construct array of board result in each column
        column = []
        # iterate each row and grab element in column base on "col"
        for row in board:
            column.append(row[col])
        
        # finish 1 column then check result
        if all_same(column):
            player_side = column[0]
            return player_side # winner
        

            
    # check horizontal
    # can use whole row in each iteration to construct the scheck array
    for row in board:
        check_list = row
        if all_same(check_list):
            player_side = check_list[0]
            return player_side # winner


    # check diagonal

    # check \ way
    # grab element 0,0 1,1 2,2 ....
    diag_array = []
    
    for i ,row in enumerate(board):
        for j , col in enumerate(row):
            if i == j:
                diag_array.append(col)

    if all_same(diag_array):
        player_side = diag_array[0]
        return player_side # winner

    # check / way
    # grab element 0,2 1,1 2,0 ....
    # i count up 1 in each iteration from 0 to the size-1 of the board....
    # so i is iteration in for loop >>>> 0 1 2
    # j count down 1 in each iteration from the size-1 of the board to 0 ...
    # j is reverse >>>> 2 1 0 

    reverse_diag_array = []

    #len(board) = number of row >>> board is rectagle row = column = size >>> 3x3 = 3
    # range(len(board)) return iterator of size board >> 0 1 2
    # reversed(range(len(board))) return reversed iterator >>> 2 1 0
    # enemerate(reversed(range(len(board)))) return number of itertion 0 1 2 for use with i 
    for i , j in enumerate(reversed(range(len(board)))):
        reverse_diag_array.append(board[i][j])
    
    if all_same(reverse_diag_array):
        player_side = reverse_diag_array[0]
        return player_side # winner



    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Tie condition check first
    # If all cell occupie that is not none then it a tie
    tie_count = 0
    for row in board:
        if EMPTY not in row:
            tie_count += 1
    if tie_count == len(board):
        return True # Game over

    # Game over is know by either X or O from  winner function
    if winner(board) != None:
        return True
    # if recieve None that mean game is still in progess
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Given board is any state

    def max_value(board):
        v = -100
        # Base case of recursive
        optimal_action = ()
        if terminal(board):
            return utility(board) , optimal_action
        for possible_action in actions(board):
            # compare the current value with return value if choose this action
            # And choose maximum value of the action of the possible case from min player
            # max() function return largest value between two value
            min_val = min_value(result(board,possible_action))[0]
            if min_val > v:
                v = min_val
                optimal_action = possible_action
            return v , optimal_action

    def min_value(board):
        v = 100
        # Base case of recursive
        optimal_action = ()
        if terminal(board):
            return utility(board) , optimal_action
        for possible_action in actions(board):
            # compare the current value with return value if choose this action
            # And choose minimum value of the action of the possible case from min player
            # Min() function return smallest value between two value
            max_val = max_value(result(board,possible_action))[0]
            if max_val < v:
                v = max_val
                optimal_action = possible_action
            return v , optimal_action


    # if this is a terminal board return None
    if terminal(board):
        return None
    
    # Check current player
    current_player = player(board)

    if current_player == X:
        # Player X Choose to Max the value
        # Choose the highest value of Min-value player
        return max_value(board)[1]
    else:
        # Player O Choose to Min the value
        # Choose the lowest value of Max-value player
        return min_value(board)[1]
