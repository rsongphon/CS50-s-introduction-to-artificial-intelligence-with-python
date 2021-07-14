from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(

    # From assumsion knowledge0 muse entail AKnave
    # By mean that all of the knowledge in this must be true

    # Structture of puzzle
    Not(And(AKnight,AKnave)), # A cannot be knight and knave at  the same time
    Or(AKnight,AKnave), # A must be knight or knave 

    # information about what the characters actually said.
    # If A is a knight then A say "I am both a knight and a knave."  has to be true
    
    Implication(AKnight,And(AKnight,AKnave)),

    # If A is a Knave then A say "I am both a knight and a knave." is false
    Implication(AKnave,Not(And(AKnight,AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    # assumption
    # A say we are both knave , since knave will always tell the lie
    # A cannot be knight because he say truth but he say he is "knave" conflict
    # So he will lie that both of them are knave
    # B must be knight

    # Structure of puzzle
    Not(And(AKnight,AKnave)), # A cannot be knight and knave at  the same time
    Or(AKnight,AKnave), # A must be knight or knave 

    # Structure of puzzle
    Not(And(BKnight,BKnave)), # B cannot be knight and knave at  the same time
    Or(BKnight,BKnave), # B must be knight or knave 

    # if A is a knight > he will say true
    Implication(AKnight,And(AKnave,BKnave)),

    # if A is a knave > he will say false
    Implication(AKnave,Not(And(AKnave,BKnave))),


)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    # Structure of puzzle
    Not(And(AKnight,AKnave)), # A cannot be knight and knave at  the same time
    Or(AKnight,AKnave), # A must be knight or knave 

    # Structure of puzzle
    Not(And(BKnight,BKnave)), # B cannot be knight and knave at  the same time
    Or(BKnight,BKnave), # B must be knight or knave 
    

    # A says We are the same kind means
    # A and B are knight or A and B are Knave
    # And(AKnight,BKnight)
    # And(Aknave,BKnave)
    # A and B are knight or A and B are Knave >>>> Or(And(AKnight,BKnight),And(Aknave,BKnave))

    # if A is a knight > he will say true
    Implication(AKnight,Or(And(AKnight,BKnight),And(AKnave,BKnave))),

    # if A is a knave > he will say false
    Implication(AKnave,Not(Or(And(AKnight,BKnight),And(AKnave,BKnave)))),

    # B says We are of different kinds
    # So it will be A are knight and B are Knave
    # And(AKnight,BKnave)
    # Or A are knave and B are Knight
    # And(AKnave,BKnight)
    # >>>> Or(And(AKnight,BKnave),And(AKnave,BKnight))

    # if B is a knight > he will say true
    Implication(BKnight,Or(And(AKnight,BKnave),And(AKnave,BKnight))),

    # if B is a knave > he will say false
    Implication(BKnave,Not(Or(And(AKnight,BKnave),And(AKnave,BKnight)))),
    

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    # Structure of puzzle
    Not(And(AKnight,AKnave)), # A cannot be knight and knave at  the same time
    Or(AKnight,AKnave), # A must be knight or knave 

    # Structure of puzzle
    Not(And(BKnight,BKnave)), # B cannot be knight and knave at  the same time
    Or(BKnight,BKnave), # B must be knight or knave 

    # Structure of puzzle
    Not(And(CKnight,CKnave)), # C cannot be knight and knave at  the same time
    Or(CKnight,CKnave), # C must be knight or knave 


    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Or
    (
        # A say 'I am a knight'
        # If A say this A might be knight or knave
            # if A is a knight > he will say true
            #Implication(AKnight,AKnight),

            # if A is a knave > he will say false
            #Implication(AKnave,Not(AKnight)),

            # both must be true that knight alway tell truth knave will alway tell lie
            And(
                Implication(AKnight,AKnight),
                Implication(AKnave,Not(AKnight))
            ),

        # A say 'I am a knave'
        # If A say this A might be knight or knave
            # if A is a knight > he will say true
            #Implication(AKnight,AKnave),
            # if A is a knave > he will say false
            #Implication(AKnave,Not(AKnave)),

            # both must be true that knight alway tell truth knave will alway tell lie
            And(
                Implication(AKnight,AKnave),
                Implication(AKnave,Not(AKnave))
            )

    ),

    # B says "A said 'I am a knave'." <<<< this massage can be get from sentence above

    # case 1 B is knight
    Implication (BKnight,

                And(
                Implication(AKnight,AKnave),
                Implication(AKnave,Not(AKnave))
                )

                ),

    # case 2 B is knave 
    Implication (BKnave,
                Not(
                And(
                Implication(AKnight,AKnave),
                Implication(AKnave,Not(AKnave))
                )
                )
                ),


    # B says "C is a knave."
    # case 1 B is knight

    Implication(BKnight,CKnave),

    # case 2 B is knave
    Implication(BKnave,Not(CKnave)),


    # C says "A is a knight."

    # C is a knight
    Implication(CKnight,AKnight),

    # C is a knave

    Implication(CKnave,Not(AKnight)),
    
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            # loop over each symbol to see if knowledge base entail which symbol
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
