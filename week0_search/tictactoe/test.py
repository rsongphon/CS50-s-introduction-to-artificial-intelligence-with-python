import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    '''
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    '''

    return [[O, EMPTY, O],
            [X, EMPTY, O],
            [X, EMPTY, O]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0

    for row in board:
        x_count = x_count + row.count(X)
        o_count = o_count + row.count(O)
    
    if (x_count == 0) and (o_count == 0):
        return X
    elif x_count > o_count:
        return O
    elif x_count <= o_count:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board. i is row (0,1,2)j is column (0,1,2)
    """
    possible_action = set()

    for i , row in enumerate(board):
        for j , col in enumerate(row):
            if col == EMPTY:
                possible_action.add((i,j))

    return possible_action

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
        if next_board[action[0]][action[1]] != EMPTY:
            raise Exception 
        next_board[action[0]][action[1]] = player(board)
        
    except Exception as e:
        print(e)

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
        

            
    # check horiontal
    # can use whole row in each iteration to construct the scheck array
    for row in board:
        check_list = row
        if all_same(check_list):
            player_side = check_list[0]
            return player_side # winner


    # check diagonal


    return None

start_board = initial_state()

#print(player(start_board))

#print(actions(start_board))


#print(result(start_board,(1,3)))

print(winner(start_board))