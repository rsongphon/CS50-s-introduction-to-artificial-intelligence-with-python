import csv
import pandas
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    return_int = ['Administrative' , 'Informational' , 'ProductRelated' , 'Month' , 'OperatingSystems' , 'Browser' , 'Region' , 'TrafficType' , 'VisitorType' , 'Weekend']
    return_float = ['Administrative_Duration', 'Informational_Duration', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues',  'SpecialDay']
    months = ['Jan','Feb','Mar','Apr','May','June','Jul','Aug','Sep','Oct','Nov','Dec']


    with open(filename , 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data_row  = []
            for column in row:
                if column in return_int:
                    # Month should be 0 for January, 1 for February, 2 for March, etc. up to 11 for December.
                    if column == 'Month':
                        for num_month , month in enumerate(months):
                            if row[column] == month:
                                data_row.append(int(num_month))
                            
                    # VisitorType should be 1 for returning visitors and 0 for non-returning visitors.
                    elif column == 'VisitorType':
                        if row[column] == 'Returning_Visitor':
                            data_row.append(1)
                        else:
                            data_row.append(0)
                    # Weekend should be 1 if the user visited on a weekend and 0 otherwise.
                    elif column == 'Weekend':
                        if row[column] == 'TRUE':
                            data_row.append(1)
                        else:
                            data_row.append(0)
                    else:
                        data_row.append(int(row[column]))

                # return float for the rest
                elif column in return_float:
                    data_row.append(float(row[column]))

                # Each value of labels should either be the integer 1, if the user did go through with a purchase, or 0 otherwise.
                else:
                    if row[column] == 'TRUE':
                        labels.append(1)
                    else:
                        labels.append(0)

                    #print(column)
                    #data_row.append(int(row[column]))
                    #print(data_row)
            evidence.append(data_row)


    print(evidence[-1])
    print(labels[-1])
    return evidence,labels

'''
def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).
    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)
    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    evidence = []
    labels = []

    months = {'Jan': 0,
              'Feb': 1,
              'Mar': 2,
              'Apr': 3,
              'May': 4,
              'June': 5,
              'Jul': 6,
              'Aug': 7,
              'Sep': 8,
              'Oct': 9,
              'Nov': 10,
              'Dec': 11}

    # read csv file
    csv_file = pandas.read_csv(filename)

    # prepare labels dataframe
    labels_df = csv_file['Revenue']

    # prepare evidence dataframe
    evidence_df = csv_file.drop(columns=['Revenue'])

    # replace month names with numerical values
    evidence_df = evidence_df.replace(months)

    # replace boolean with 0/1 values
    evidence_df['VisitorType'] = evidence_df['VisitorType'].apply(lambda x: 1 if x == 'Returning_Visitor' else 0)
    evidence_df['Weekend'] = evidence_df['Weekend'].apply(lambda x: 1 if x == 'True' else 0)
    labels_df = labels_df.apply(lambda x: 1 if x is True else 0)

    # convert dataframes to lists
    evidence_list = evidence_df.values.tolist()
    print(evidence_list[-1])
    labels_list = labels_df.values.tolist()
    print(labels_list[-1])

    return evidence_list, labels_list
'''


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(evidence, labels)
    return neigh



def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    actual_buy_total = 0
    actual_buy_correct = 0
    actual_notbuy_total = 0
    actual_notbuy_correct = 0
    for actual , predict in zip(labels,predictions):
        # sensitivity should be a floating-point value from 0 to 1 representing the “true positive rate”
        if actual == 1:
            actual_buy_total += 1
            if predict == actual:
                actual_buy_correct += 1
        # specificity should be a floating-point value from 0 to 1 representing the “true negative rate”
        else:
            actual_notbuy_total += 1
            if predict == actual:
                actual_notbuy_correct += 1
    
    sensitivity = float(actual_buy_correct)/actual_buy_total
    specificity = float(actual_notbuy_correct)/actual_notbuy_total

    return sensitivity,specificity

        
    #raise NotImplementedError


if __name__ == "__main__":
    main()
