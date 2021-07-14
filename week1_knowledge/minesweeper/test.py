height = 8
width = 8


cell = (4,4)

neighbour_set = set()

for i in range(cell[0]-1,cell[0]+2): # row
    for j in range(cell[1]-1,cell[1]+2):

        # not inclue the cell it self
        if (i,j) == cell:
            continue

        '''
        cell must in the region of  the board
        that is 
        row  >= 0 (row[0]) but < self.height ex: 0-7
        column >= 0 (row[0]) but < self.width  ex: 0-7
        '''

        if (0 <= i <= height) and (0 <= j <= width):
            neighbour_set.add((i,j))

print(neighbour_set)

count =1

def known_safes():
    """
    Returns the set of all cells in self.cells known to be safe.
    """
    '''
    If self.count = 0 
    Then all cell in this sentence are not mine

    '''

    if count == 0:
        return 1


print(known_safes())