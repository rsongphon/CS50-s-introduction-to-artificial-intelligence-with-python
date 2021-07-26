import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                #print(people)
                p = joint_probability(people, one_gene, two_genes, have_trait)
                #p = joint_probability(people, {"Harry"}, {"James"}, {"James"})
                
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # intial value 
    joint_prob_dist = 1
    # Note that all value is multiplication , order does not matter (except child that have sum!)


    for person in people:
        # prob frome gene

        if (person in one_gene) or (person in two_genes):
            # check if it mother, father or child

            # if mother or father ----> thier 'mother','father' in people == None
            if (people[person]['mother'] == None and people[person]['father'] == None) and (person in one_gene):
                # grap prob of 1 gene
                joint_prob_dist = joint_prob_dist*PROBS['gene'][1]
                print(person + ' has 1 gene with propability of ' + str(PROBS['gene'][1]))

            elif (people[person]['mother'] == None and people[person]['father'] == None) and (person in two_genes):
                # grap prob of 1 gene
                joint_prob_dist = joint_prob_dist*PROBS['gene'][2]
                print(person + ' has 2 gene with propability of ' + str(PROBS['gene'][2]))

            # if child ---> thier 'mother','father' in people != None
            else:
                # either get this from his mother and not his father, 
                # and he gets the gene from his father and not his mother
                # sum both 2 case

                # case 1 get from his mother and not his father,
                # check mother gene
                if (people[person]['mother'] not in one_gene) and (people[person]['mother'] not in two_genes):
                    # mutation from  0 gene
                    case1_prob_from_mother =  PROBS['mutation'] # 0.01
                    case1_prob_from_father = 1 - PROBS['mutation'] # 0.99
                else:
                    # mother has 1 or two gene 
                    # not mutate
                    case1_prob_from_mother =  1 - PROBS['mutation'] # 0.99 
                    case1_prob_from_father =  PROBS['mutation'] # 0.01
                
                # case 2 gets the gene from his father and not his mother
                # check father gene

                if (people[person]['father'] not in one_gene) and (people[person]['father'] not in two_genes):
                    # mutation from  0 gene
                    case2_prob_from_father =  PROBS['mutation'] # 0.01
                    case2_prob_from_mother =  1 - PROBS['mutation']# 0.99
                    
                else:
                    # father has 1 or two gene 
                    # not mutate
                    case2_prob_from_father =  1 - PROBS['mutation'] # 0.99
                    case2_prob_from_mother = PROBS['mutation']  # 0.01
                    
                # sum 2 case together
                #print(case1_prob_from_mother , case1_prob_from_mother , case1_prob_from_father , case2_prob_from_father)
                sum_prob = (case1_prob_from_mother * case2_prob_from_mother) + (case1_prob_from_father * case2_prob_from_father)
                print(person + ' is a child has gene with propability of ' + str(sum_prob))

                joint_prob_dist = joint_prob_dist*sum_prob

        else: # 0 genes
            # parent
            if (people[person]['mother'] == None and people[person]['father'] == None):
                # grap prob of 1 gene
                joint_prob_dist = joint_prob_dist*PROBS['gene'][0]
                print(person + ' has 0 gene with propability of ' + str(PROBS['gene'][0]))

            # child
            # if child ---> thier 'mother','father' in people != None
            else:
                # either get this from his mother and not his father, 
                # and he gets the gene from his father and not his mother
                # sum both 2 case

                # case 1 get from his mother and not his father,
                # check mother gene
                if (people[person]['mother'] not in one_gene) and (people[person]['mother'] not in two_genes):
                    # not mutate
                    case1_prob_from_father =  PROBS['mutation'] # 0.01
                    case1_prob_from_mother = 1 - PROBS['mutation'] # 0.99
                else:
                    # mother has 1 or two gene 
                    # mutate
                    case1_prob_from_father =  1 - PROBS['mutation'] # 0.99 
                    case1_prob_from_mother =  PROBS['mutation'] # 0.01
                
                # case 2 gets the gene from his father and not his mother
                # check father gene

                if (people[person]['father'] not in one_gene) and (people[person]['father'] not in two_genes): # father 0
                    # father 0 not mutate
                    case2_prob_from_mother =  PROBS['mutation'] # 0.01
                    case2_prob_from_father =  1 - PROBS['mutation']# 0.99
                    
                else:
                    # father has 1 or two gene 
                    # mutate
                    case2_prob_from_mother =  1 - PROBS['mutation'] # 0.99
                    case2_prob_from_father = PROBS['mutation']  # 0.01
                    
                # sum 2 case together
                sum_prob = (case1_prob_from_mother * case2_prob_from_mother) + (case1_prob_from_father * case2_prob_from_father)
                print(person + ' is a child has gene with propability of ' + str(sum_prob))

                joint_prob_dist = joint_prob_dist*sum_prob

        # prob from trait
        if person in have_trait:
            if person in one_gene:
                joint_prob_dist = joint_prob_dist*PROBS["trait"][1][True]
                print(person + ' has 1 gene with trait and propability of ' + str(PROBS["trait"][1][True]))
            elif person in two_genes:
                joint_prob_dist = joint_prob_dist*PROBS["trait"][2][True]
                print(person + ' has 2 gene with trait and propability of ' + str(PROBS["trait"][2][True]))
            else:
                joint_prob_dist = joint_prob_dist*PROBS["trait"][0][True]
                print(person + ' has 0 gene with trait and propability of ' + str(PROBS["trait"][0][True]))
        else:
            if person in one_gene:
                joint_prob_dist = joint_prob_dist*PROBS["trait"][1][False]
                print(person + ' has 1 gene with no trait and propability of ' + str(PROBS["trait"][1][False]))
            elif person in two_genes:
                joint_prob_dist = joint_prob_dist*PROBS["trait"][2][False]
                print(person + ' has 2 gene with no trait and propability of ' + str(PROBS["trait"][2][False]))
            else:
                joint_prob_dist = joint_prob_dist*PROBS["trait"][0][False]
                print(person + ' has 0 gene with no  trait and propability of ' + str(PROBS["trait"][0][False]))
        
        #print(person + ': ' + str(joint_prob_dist))

    print(joint_prob_dist)
    return joint_prob_dist 

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for people in probabilities:
        if people in one_gene:
            probabilities[people]['gene'][1] = probabilities[people]['gene'][1] + p
        elif people in two_genes:
            probabilities[people]['gene'][2] = probabilities[people]['gene'][2] + p
        
        if people in have_trait:
            probabilities[people]["trait"][True] = probabilities[people]["trait"][True] + p
    
    print(probabilities)



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    


if __name__ == "__main__":
    main()
