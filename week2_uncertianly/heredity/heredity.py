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
        if person in one_gene:
            gene_num = 1
        elif person in two_genes:
            gene_num = 2
        else:
            gene_num = 0
        
        if person in have_trait:
            trait = True
        else:
            trait = False

        # if no parent data  use joint prob distrubuiton
        if people[person]['mother'] == None:
            joint_prob_dist = joint_prob_dist * PROBS['gene'][gene_num] * PROBS['trait'][gene_num][trait]

        # child 
        else:
            # create dictionary to keep passing percentage
            percent_passing = {}

            '''
            # if person has 2 genes they will pass to child but with 99 % (other case is 1 % mutation no passing)
            # if person has 1 genes they will pass to child but with 50 % 
            # if person has 0 genes they still can pass gene to child  1%  (mutation)
            '''
            # Father passing percentage
            if people[person]['father'] in two_genes:
                percent_passing['father'] = 1 - PROBS['mutation'] # 0.99
            elif people[person]['father'] in one_gene:
                percent_passing['father'] = 0.5 # 50% pass
            else:
                percent_passing['father'] = PROBS['mutation'] # 0.01

            # Mother passing percentage
            if people[person]['mother'] in two_genes:
                percent_passing['mother'] = 1 - PROBS['mutation'] # 0.99 pass
            elif people[person]['mother'] in one_gene:
                percent_passing['mother'] = 0.5  # 50 % pass
            else:
                percent_passing['mother'] = PROBS['mutation'] # 0.01 mutation case

            # check case for child
            '''
            # if child has 2 gene num ----> both parent are passing 1 copy 
            # if child has 1 gene num  ---->  2 case  sumup
                # 1. Mother pass gene, Father not
                # 2. Father pass gene, Mother not
            # if child has 0 gene ----> not passing from both parent
            
            '''
            temp_prob = 1

            if gene_num == 2:
                print(f'Child : {person} has {gene_num} gene')
                print(f'Mother passing  ' + str(percent_passing['mother']))
                print(f'Father passing  ' + str(percent_passing['father']))
                temp_prob *= percent_passing['father']*percent_passing['mother']
                temp_prob *= PROBS['trait'][gene_num][trait]
            elif gene_num == 1:
                print(f'Child : {person} has {gene_num} gene')
                print(f'Mother passing  ' + str(percent_passing['mother']))
                print(f'Father passing  ' + str(percent_passing['father']))
                temp_prob *= ((percent_passing['mother']*(1-percent_passing['father'])) + (percent_passing['father']*(1-percent_passing['mother'])))
                temp_prob *= PROBS['trait'][gene_num][trait]
            else:
                print(f'Child : {person} has {gene_num} gene')
                print(f'Mother passing  ' + str(percent_passing['mother']))
                print(f'Father passing  ' + str(percent_passing['father']))
                temp_prob *= (1-percent_passing['father']) * (1-percent_passing['mother'])
                temp_prob *= PROBS['trait'][gene_num][trait]
            
            joint_prob_dist *= temp_prob

        
        #print(joint_prob_dist)
            
    return joint_prob_dist 

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        gene_number = 1 if person in one_gene else 2 if person in two_genes else 0
        probabilities[person]["gene"][gene_number] += p
        probabilities[person]["trait"][person in have_trait] += p

    print(probabilities)



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    '''
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

    '''
    # To normalize sum to 1
    # sum of the all element
    # devide each element by sum

    # normalize gene
    for person  in probabilities:
       for type in probabilities[person]:
            sum = 0
            for element in probabilities[person][type].values():
                sum += element
            for key in probabilities[person][type].keys():
                probabilities[person][type][key] /= sum

    

    
if __name__ == "__main__":
    main()
