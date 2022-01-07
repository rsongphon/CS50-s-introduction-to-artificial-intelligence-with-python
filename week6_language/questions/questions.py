import nltk
import sys
import os
import string
import copy
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    corpus_path = os.path.join(os.getcwd(),directory)
    file_text = {}

    for filename in os.listdir(directory):
        file_path = os.path.join(corpus_path,filename)
        with open(file_path,'r',encoding="utf8") as file:
            text = file.read()
        file_text[filename] = text
    
    return file_text



def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # string.punctuation = '!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~' >>>> list(string.punctuation)
    # nltk.corpus.stopwords.words("english") return a list of  stopword
    word_tokenize = nltk.word_tokenize(document)
    
    filter_word = []
    for word in word_tokenize:
        word = word.lower()
        if word in list(string.punctuation): # filter out punctuation 
            continue
        elif word in nltk.corpus.stopwords.words("english"): # filter out stopword
            continue
        else:
            filter_word.append(word)
    
    return filter_word

    


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    num_document = float(len(documents))

    already_count_word = [] # keep the word that has been calculate idf
    word_idf = {}

    for filetext in documents:
        for word in documents[filetext]:
            # new word found
            if word not in already_count_word:
                already_count_word.append(word)
                num_doucument_contain_word = 0
                # count the number of document that contian that word
                for document in documents:
                    if word in documents[document]:
                        num_doucument_contain_word += 1
                # compute idf
                word_idf_value = math.log(num_document/num_doucument_contain_word)
                word_idf[word] = word_idf_value
    
    return word_idf



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    '''
    Files should be ranked according to the sum of tf-idf values for any word in the query 
    that also appears in the file. Words in the query that do not appear in the file 
    should not contribute to the file’s score.
    '''
    file_tf_idf = {}
    file_rank = []

    '''
    psedocode 

    for eachfile
    initial sum of tf-idf score = 0
        for each word in query
            count the word in file as tf
            calcuate tf-idf of the word
            add to sum of tf-idf 
    store sum of to sum of tf-idf score to dictionaty by filename

    '''
    for filename in files:
        tf_idf_sum = 0
        for word in query:
            # tf
            word_count = files[filename].count(word)
            if word_count == 0:
                continue
            tf_idf = word_count*idfs[word]
            tf_idf_sum += tf_idf

        file_tf_idf[filename] = tf_idf_sum
    
    # sort dictionary 
    file_tf_idf = {k: v for k, v in sorted(file_tf_idf.items(), key=lambda item: item[1],reverse=True)}
    #print(file_tf_idf)

    for i,filename in enumerate(file_tf_idf):
        if i < n:
            file_rank.append(filename)
    #print(file_rank)
    return file_rank

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    '''Sentences should be ranked according to “matching word measure”: namely, the sum of IDF values for any word in the query 
    that also appears in the sentence. Note that term frequency should not be taken into account here, 
    only inverse document frequency.'''

    '''
    psuedo code
    for each sentence
    initial sum of sentence idf = 0
        for each word in query
        if word in sentence
            add idf of word to sum of sentence
    '''
    sentences_score = {}
    sentences_rank = []
    

    for sentence in sentences:
        idf_sum = 0
        for word in query:
            if word in sentences[sentence]:
                idf_sum+= idfs[word]
        

        if idf_sum != 0:
            query_word = 0
            for word in query:
                if word in sentences[sentence]:
                    query_word += 1
            density = query_word / len(sentence)
            sentences_score[sentence] = (idf_sum,density)

    # sort dictionary 
    sentences_score = {k: v for k, v in sorted(sentences_score.items(), key=lambda item: (item[1][0],item[1][1]),reverse=True)}
    print(sentences_score)

    for i,sentence_name in enumerate(sentences_score):
        if i < n:
            sentences_rank.append(sentence_name)
    print(sentences_rank)
    #return file_rank



if __name__ == "__main__":
    main()
