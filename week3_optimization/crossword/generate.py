import sys


from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()

        '''
        for test to see overlap variable
        for var in self.crossword.variables:
            print(f'{var} overlap with {self.crossword.neighbors(var)}')
        
        ''' 
        '''
        for test revise function
        #print(self.crossword.variables)
        #self.revise(Variable(4, 4 ,'across', 5),Variable(1, 7, 'down', 7))
        #self.revise(Variable(2, 1 ,'down', 5),Variable(2, 1, 'across', 12))
        self.revise(Variable(2, 1, 'across', 12),Variable(1, 7, 'down', 7))
        '''
        
        self.ac3()

        

        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        '''
        psuedo code
        loop for every variable in crossword puzle (self.crossword.variables)
            loop for every word in that variabel domain  (self.domains[var])
                if lenght of word in domain != lenght of that variable
                    remove that word
        '''
        for var in self.crossword.variables:
            word_domain_copy = self.domains[var].copy() # copy set of domain word
            for word in self.domains[var]:
                if len(word) != var.length:
                    word_domain_copy.remove(word)
            self.domains[var] = word_domain_copy
            #print(f'{var.length} : {self.domains[var]}')
        
    

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        '''
        in crossword if 2 variable have overlap each other
        it must be the same letter.

        A word that x have must have the same letter in word in y domain in the same location

        ** remove word in x that have dirrent letter in same  location of y **

        '''
        '''
        crossword.overlaps is a dictionary mapping a pair of variables to their overlap. For any two distinct variables v1 and v2, 
        crossword.overlaps[v1, v2] will be None if the two variables have no overlap, and will be a pair of integers (i, j) 
        if the variables do overlap. The pair (i, j) should be interpreted to mean that the ith character of v1’s value must be the 
        same as the jth character of v2’s value.
        
        '''
        revise = False

        x_domain_copy = self.domains[x].copy()
        #print(x_domain_copy)

        # check to see if x overlap with y
        if self.crossword.overlaps[x,y] != None:
            
            # overlap
            #  ith character of X value
            # same as the jth character of y
            i , j = self.crossword.overlaps[x,y]
            #print(f'Overlap at i:{i}, j:{j}')
            word_keep = set()
            for x_word in  self.domains[x]:
                for y_word in self.domains[y]:
                    #if ith character of X value same as jth character of y >> keep word for domain x
                    if x_word[i] == y_word[j]:
                        #print(f'x word: {x_word}   y word: {y_word}')
                        #print(f'keep word {x_word}')
                        word_keep.add(x_word)
                        
            
            if len(word_keep) != 0:
                for word in  self.domains[x]:
                    if word not in word_keep:
                        x_domain_copy.remove(word)
                        revise = True
        
        self.domains[x] = x_domain_copy
        #print(self.domains[x])
        return revise





    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        # if initail state that arc is none Queue the arc
        # where each arc is a tuple (x, y) of a variable x and a different variable y
        # queue = list of all edge
        if arcs == None:
            queue = []
            queue_match = {}

            # keep track of edge
            for var in self.crossword.variables:
                queue_match[var] = []
            
            for var in self.crossword.variables:
                #print(f'{var} : neighbour',end='')
                #print(self.crossword.neighbors(var))
                neighbour = self.crossword.neighbors(var)
                for neighbour in neighbour:
                    # if already have edge with other , skip
                    if var in queue_match[neighbour]:
                        continue
                    else:
                    # add edge
                        queue_match[var].append(neighbour)
                        queue.append((var,neighbour)) 

            #print(len(queue))
        while len(queue) != 0:
            # Dequeue
            x,y = queue.pop(0)
            # Apply arc consistency
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                neighbour = self.crossword.neighbors(x)
                for neighbour in neighbour:
                    if neighbour == y:
                        continue
                    else:
                        queue.append((neighbour,x))
        ''' for testing
        for var in self.domains:
            print(f'{var} : {self.domains[var]} ')
        '''

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        '''
        An assignment is a dictionary where the keys are Variable objects and the values are strings 
        representing the words those variables will take on
        '''
        for var in assignment:
            # all values are distinct
            for other_var in assignment:
                # skip the value itself
                if var == other_var:
                    continue
                else:
                    if assignment[var] == assignment[other_var]:# same string
                        return False
        

            # every value is the correct length
            if len(assignment[var]) != var.length:
                return False

            #  no conflicts between neighboring variables
            neighbour = self.crossword.neighbors(var)
            for neighbour in neighbour:
                # check if neighbour is already assign
                if neighbour not in assignment:
                    continue
                else:
                    i ,j  = self.crossword.overlaps[var,neighbour]
                    if assignment[var][i] != assignment[neighbour][j]:
                        return False

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # implementing first for random order
        domain_list = list(self.domains[var])
        return domain_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        for var in self.crossword.variables:
            if var in assignment:
                continue
            else:
                return var
        return None

    
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # if finished return assigment dict
        if self.assignment_complete(assignment):
            return assignment

        # select unassign variable
        var = self.select_unassigned_variable(assignment)

        # value in domain value of that variable
        domain = self.order_domain_values(var,assignment)

        for word in domain:
            new_assignment = assignment.copy()
            new_assignment[var] = word

            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        
        return None




def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
