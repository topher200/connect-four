# display characters
BLANK_STR = '   '
PLAYER_1_STR = ' X '
PLAYER_2_STR = ' O '
LEFT_PAD_STR = '   '
HORIZ_BOARD_STR = '-'
HORIZ_BOARD_STR_THREE = ''.join(HORIZ_BOARD_STR for x in xrange(3))
VERTICAL_BOARD_STR = '|'
assert len(BLANK_STR) == len(PLAYER_1_STR) == len(PLAYER_2_STR)

def get_board_display(board_state, debug_mode=False):
    """
        The L{board_state} must be a 2-dimensional array (list of lists)
        where each positional value is what should be printed in the
        corresponding cell.

        Returns a string representation of the board state.  Always
        has number labels on the columns.  

        If L{debug_mode} is C{True}, the column number labels will 
        be zero-based (0...NUM_COLS) and 0-based row labels
        will be present.  If C{debug_mode} is C{False}, the column labels
        will be 1-based (1...NUM_COLS+1) and there will be no row labels.

        Example (debug mode):
             0   1   2   3   4   5   6   7   8   9
           |---|---|---|---|---|---|---|---|---|---|
         0 |   |   |   |   |   |   |   |   |   |   |
         1 |   |   |   |   |   |   |   |   |   |   |
         2 |   |   |   |   |   |   |   |   |   |   |
         3 |   |   |   |   |   |   |   |   |   |   |
         4 |   |   |   |   |   |   |   |   |   |   |
         5 |   |   |   |   |   |   |   |   |   |   |
         6 |   |   |   |   |   |   |   |   |   |   |
         7 |   |   |   |   |   |   |   |   |   |   |
           |---|---|---|---|---|---|---|---|---|---|

    """
    assert isinstance(board_state, list) # better be a list
    assert isinstance(debug_mode, bool) # better be a boolean
    # detect the board dimensions
    board_height = len(board_state)
    assert board_height >= 1
    # just asserted there is at least 1 element, grab it to detect width
    board_width = len(board_state[0]) 
     # make sure 2d array is rectangular
    assert all(len(cols) == board_width for cols in board_state)

    # make the base of the string that will 
    # represent the top and bottom of the board.
    # the statement 'STR_1.join(iterable)'' will join each element 
    # from the iterable using STR_1
    # for example, 'm'.join(('1','2','3','4')) will create the string
    # 1m2m3m4
    # NOTE: it doesn't put one before or after, so we do it manually.
    BASE_TOP_BOT = (LEFT_PAD_STR + # indent the top line by the pad
                    VERTICAL_BOARD_STR + # add one before
                    # this join uses a shortcut syntax for defining an iterable,
                    # the innards of the join(stuff to join) will yield an iterable
                    # the same length as the xrange (which we're using just to
                    # count iterations) but with every element as '---'
                    VERTICAL_BOARD_STR.join(HORIZ_BOARD_STR_THREE for x in xrange(board_width)) + 
                    VERTICAL_BOARD_STR + # add one after
                    '\n')

    # debug mode shows the 0-based indices of the columns, but 
    # when we're playing the game we use 1 to len(cols)
    if debug_mode:
        col_labels = xrange(0, board_width)
    else:
        col_labels = xrange(1, board_width + 1)

    # the line with the numbers labelling the columns
    HEADER = ('\n' + 
              LEFT_PAD_STR + 
              # this next one labels the columns
              ' '.join('%3d' % x for x in col_labels) + 
              '\n' +
              BASE_TOP_BOT)

    FOOTER = '' # just in case we want to add feet or something

    board_display_string = '' # build this string as we go
    board_display_string += HEADER

    # for each row in the grid, print the grid lines
    # with the contents of any cell injected into them.
    for idx, row_cell_list in enumerate(board_state):
        if debug_mode:
            # add the row counter
            board_display_string += '%2d ' % idx
        else:
            board_display_string += LEFT_PAD_STR

        board_display_string += (VERTICAL_BOARD_STR +
                                 VERTICAL_BOARD_STR.join(row_cell_list) +
                                 VERTICAL_BOARD_STR +
                                 '\n')

        board_display_string += BASE_TOP_BOT

    board_display_string += FOOTER

    return board_display_string
# end of the function: get_board_state

def get_next_free_row_in_column(col_number, board_state):
    """
        Calculate and return the row index.
        indicating the next available cell in the given L{col_number}.
        All row/col indices this deals with are zero-based.

        DO NOT ALTER L{board_state} in this function!
    """
    assert isinstance(col_number, int) # better be an integer
    assert isinstance(board_state, list)

    board_height = len(board_state)
    assert board_height >= 1
    # just asserted there is at least 1 element, grab it to detect width
    board_width = len(board_state[0]) 
     # make sure 2d array is rectangular
    assert all(len(cols) == board_width for cols in board_state)

    # from max row index (height - 1) to 0 (to -1, not inclusive!), by -1
    for row_idx in xrange(board_height-1, -1, -1): 
        if board_state[row_idx][col_number] == BLANK_STR:
            return row_idx # return as soon as we find an empty cell

    # never found an empty cell
    return None

def get_next_player(current_player):
    assert isinstance(current_player, str)

    if current_player == PLAYER_1_STR:
        return PLAYER_2_STR

    assert current_player == PLAYER_2_STR
    return PLAYER_1_STR

def is_board_full(board_state):
    assert isinstance(board_state, list) # better be a list
    assert isinstance(debug_mode, bool) # better be a boolean
    # detect the board dimensions
    board_height = len(board_state)
    assert board_height >= 1
    # just asserted there is at least 1 element, grab it to detect width
    board_width = len(board_state[0]) 
     # make sure 2d array is rectangular
    assert all(len(cols) == board_width for cols in board_state)

    for row in board_state:
        for col_value in row:
            if col_value == BLANK_STR:
                 # as soon as you find any open spot, return
                 # that the board is NOT full
                return False

    # if we make it here, we never found an empty spot,
    # so the board must be full
    return True 

# create the board state that will track th
board_state = []
BOARD_HEIGHT = 6 # standard is 6
BOARD_WIDTH = 7 # standard is 7

for x_idx in xrange(BOARD_HEIGHT):
    board_state.append([BLANK_STR for x in xrange(BOARD_WIDTH)])

# # toss a few dummy values in here to demonstrate where they land
# board_state[0][0] = PLAYER_1_STR
# board_state[0][1] = PLAYER_1_STR
# board_state[3][5] = PLAYER_2_STR
# board_state[3][6] = PLAYER_2_STR

# show the board
print(get_board_display(board_state))
# player 1 goes first
current_player = PLAYER_1_STR

while not is_board_full(board_state): 

    # raw_input will not return a value until a user enters it
    # into the terminal that called this script.  The returned
    # value is always a string, even if it's composed of numbers! 
    col_input = raw_input('Player%sPick a column, 1-%s: ' % (current_player, BOARD_WIDTH))

    # this is a way of handling errors.  If anything in the 'try' block
    # goes BOOM, the 'except' block is executed.  This is generally a bad
    # idea, but when used carefully can be really helpful.
    try:
        # try to slam the input string into an integer.  If
        # not possible, BOOM
        col_num = int(col_input) - 1 # display to user is offset by one!!!
    except: 
        print('Invalid column number')
        continue # stops executing this iteration of the loop and goes back to the top

    assert isinstance(col_num, int)

    # handle illegal column integers.
    if col_num >= BOARD_WIDTH:
        print('Column number must be between 1 and %s, you gave %s' % (BOARD_WIDTH, col_input))

    # add something to the specified column
    row_to_add = get_next_free_row_in_column(col_num, board_state) # won't work, just for example
    if row_to_add is not None:
        board_state[row_to_add][col_num] = current_player
    else:
        print('Column %s is full! pick again' % col_input)
        continue

    # update the current player.
    current_player = get_next_player(current_player)

    # finally, print the board state so that the next players
    # turn reflects the latest state
    print(get_board_display(board_state))

# end loop if the board is full
print("Are you sure no one won? If not, the board is full so it's a tie")
