import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    '''
    Sentence หมายถึงเวลาที่ AI (ผู้เล่น) คลิกที่ตำแหน่ง cell ไหนก็ตาม
    จะ return ค่าออกมาเป็น
    1. set of board cells ตำแหน่งของcells รอบจุดที่คลิกในรูปแบบ set
    3. จำนวนระเบิดที่ cells นั้นๆ

    '''

    def __init__(self, cells, count):
        # cell แต่ละ cell คือ location (i,j)
        self.cells = set(cells)  # set รับค่าเป็น array or tuple ที่ iterable ได้ และแปลงเป็น set {} EX: set((1,2),(1,3)) = {(1,2,(1,3))}
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        '''
        If the length of the set(number of element) is equal to count
        Then all of the cell must be mine 
        Ex: {E, F, H} = 3
        E , F , H is mine

        refer that 
        self.cells =  set of cell ({(i,j),(h,k),....})
        self.count = number of mine around it (interger)

        return set of all cell that is mine

        return None if no solution


        '''

        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        '''
        If self.count = 0 
        Then all cell in this sentence are not mine

        return None if no solution

        '''

        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        '''
        mark_mine update a sentence in response to new information about a cell.

        1. Remove cell from sentence
        2. decrese the count by 1 : Because cell is mine

        '''
        # Check to see If cell is in the sentence then remove from cell
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        else:
            pass


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        '''
        mark_count update a sentence in response to new information about a cell.

        1. Remove cell from sentence
        2. remain count the same because cell is safe

        '''
        if cell in self.cells:
            self.cells.remove(cell)
        else:
            pass


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        This is call when clicked

        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge: # need to remove that cell in every knowledge
            sentence.mark_mine(cell)  # It will call mark_mine(self, cell) in Sentence Class

        '''
        sentence.mark_mine(cell) is method in sentence class and update that sentence

        '''

    def mark_safe(self, cell):
        """
        This is call when clicked

        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge: # need to remove that cell in every knowledge
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        '''
         update self.mines, self.safes, self.moves_made, and self.knowledge
        '''

        '''
        
        # 1. mark the cell as a move that has been made
        # update self.moves_made

        '''
        self.moves_made.add(cell)
        '''
        
        # 2) mark the cell as safe
        # update self.safes = set()

        '''
        self.safes.add(cell)
        '''

        #3) add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`
        
        '''
        def neighbour_cell(self,cell):

            neighbour_set = set()

            '''
            Return a set of neighbour 3x3 cell 
            
            '''

            # cell is upler (i,j)
            # cell[0] = i = row , cell[1] =  j = column
            # board index must be 0 to  

            # iterate over cell
            '''
            Function range(a,b) return value from a to but not include b
            ex: cell = (4 , 5)

            i = 4
            j = 5

            row above = 3
            row below = 5

            range() must be (3,6) from row 3 to row 5 (not include 6)

            so it is range (cell[0] - 1 , cell[0]+2)

            '''
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

                    if (0 <= i <= self.height) and (0 <= j <= self.width):
                        # Be sure to only include cells whose state is still undetermined in the sentence
                        if (cell in self.mines) or (cell in self.safes):
                            pass
                        neighbour_set.add((i,j))
            
            return neighbour_set

        near_cell_set = self.neighbour_cell(cell)
        new_sentence = Sentence(near_cell_set,count)

        self.knowledge.append(new_sentence)


        '''
        # 4) mark any additional cells as safe or as mines
        # if it can be concluded based on the AI's knowledge base
        '''

        '''
        AI thinking 
        Iterate over sentence in knowledge base
        and call method known_mines() and known_mines() to check if it can be mark as safe or mine
        '''

        def check_knowledge(self,knowledge):
            for sentence in knowledge:
                # Return the set of cell that is safe or mine : None otherwise
                safe_cell_set = sentence.known_safes()
                mine_cell_set = sentence.known_mines()

                if safe_cell_set is not None:
                    #iterate over cell and mark it
                    for safe_cell in safe_cell_set:
                        self.mark_safe(safe_cell)

                elif mine_cell_set is not None:
                    #iterate over cell and mark it
                    for mine_cell in mine_cell_set:
                        self.mark_mine(mine_cell)


        self.check_knowledge(self.knowledge)


        '''
        5) add any new sentences to the AI's knowledge base
        if they can be inferred from existing knowledge
        If, based on any of the sentences in self.knowledge, new sentences
        be inferred (using the subset method described in the Background), 
        then those sentences should be added to the knowledge base as well.
        '''

        new_infer_knowledge = []

        for sentence in self.knowledge:
            # check that sentence is subset of any sentence

            '''
            set1 = count1 and set2 = count2
            where set1 is a subset of set2,
            new_set = set2 - set1 
            new_count = count2 - count1
            '''
            for compare_sentence in self.knowledge:
                if sentence.cells.issubset(compare_sentence.cells):
                    new_set = compare_sentence.cells - sentence.cells
                    new_count = compare_sentence.count - sentence.count
                    add_sentence =  Sentence(new_set,new_count)
                    new_infer_knowledge.append(new_infer_knowledge)

            # After get new sentence ->>> append to knowledge base

            self.knowledge = self.knowledge + new_infer_knowledge

            self.check_knowledge(self.knowledge) # check again for new inference


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # itrate all over the board

        for i in range(0,self.height):
            for j in range(0,self.width):
                #if move already made
                if (i,j) in self.moves_made:
                    continue
                elif (i,j) in self.mines:
                    continue
                elif (i,j) in self.safes:
                    return (i,j)

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
       
        rand_cell = []

        for i in range(0,self.height):
            for j in range(0,self.width):
                #if move already made
                if (i,j) in self.moves_made:
                    continue
                elif (i,j) in self.mines:
                    continue
                else:
                    rand_cell.append((i,j))

        if len(rand_cell) == 0:
            return None

        random_index = random.randint(0,len(rand_cell)-1)
        return rand_cell[random_index]