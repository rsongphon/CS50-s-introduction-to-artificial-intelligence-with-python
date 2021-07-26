import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    #if len(sys.argv) != 2:
    #    sys.exit("Usage: python pagerank.py corpus")
    #corpus = crawl(sys.argv[1])

    corpus = {"1.html": {"2.html", "3.html"}, "2.html": {}, "3.html": {"2.html"}}

    model = transition_model(corpus,'3.html',damping_factor=0.85)

    print(model)


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus,page,damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    '''
    The return value of the function should be a Python dictionary with 
    one key for each page in the corpus. Each key should be mapped to a value 
    representing the probability that a random surfer would choose that page next. 
    The values in this returned probability distribution should sum to 1.
    
    ex : corpus were {"1.html": {"2.html", "3.html"}, "2.html": 
    {"3.html"}, "3.html": {"2.html"}}


    return {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}
    '''

    # iterate through  each page corpus

    for current_page , link in corpus.items():
        #print (current_page , link)
        if current_page == page:
            """
            If page has no outgoing links, then transition_model should return a probability distribution 
            that chooses randomly among all pages with equal probability.
            """
            if link == {}: 
                prob_dist = {}
                for i in corpus.keys():
                    prob_dist[i] = (1/len(corpus))
                return prob_dist
            else:
                """
                1 . Dampling factor 0.85 choose random from link: ex 0.85 / number of link (equally)
                2. 1 - dampling factor choose all page in corpus random : 0.15 / number of all page

                return values should be dictionary of all page : page that have link weight more because dampling factor
                    other page weitgt by 1 - dampling factor
                """
                prob_dist = {}
                for i in corpus.keys():
                    prob_dist[i] = (1 - damping_factor) / len(corpus) # 1 - dampling factor base
                    if i not in link:
                        continue
                    else: # Dampling factor 0.85 choose random from link . add from (1 - dampling factor) base
                        prob_dist[i] = prob_dist[i] + (damping_factor / len(link))
                return prob_dist

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample_count = {}

    for page in corpus.keys():
        sample_count[page] = 0 

    print(sample_count)

if __name__ == "__main__":
    main()