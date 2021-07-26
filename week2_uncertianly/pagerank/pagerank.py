import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


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


def transition_model(corpus, page, damping_factor):
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

    page = '1.html'

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

    # first page choose at random
    current_sample_page = random.choice(list(corpus.keys()))
    n -= 1
    sample_count[current_sample_page] += 1

    # next rest sample 
    for i in range(n):
        # transition_model
        # ex prob_dist = {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}
        page_prob_dist = transition_model(corpus, current_sample_page, damping_factor)
        weight = list(page_prob_dist.values())
        # sample page :return list of lenght 1
        sample_page = random.choices(list(page_prob_dist.keys()),weights=weight)
        current_sample_page = sample_page[0]
        #print(current_sample_page)
        sample_count[current_sample_page] += 1
    
    # devide sample count by sample number to get the proportion

    pagerank = {}
    for page , count in sample_count.items():
        pagerank[page] = count/n

    return pagerank



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # First Assign page rank  by 1 /  number of page in corpus
    pagerank = {}
    for page in corpus.keys():
        pagerank[page] = 1/len(corpus)

    previous_pagerank = copy.deepcopy(pagerank)

    # (1 - d) / numpage 
    constant_prob = (1-damping_factor)/len(corpus)

    while True:
        # calculate new page rank base on formular for every page and base on previous page rank

        for page  in corpus.keys():

            sum_value = 0
            # searh for page that have a link to this page
            for search_page , link in corpus.items():
                # this page has link to 
                if page in link:
                    # grab current value of page rank
                    pagelink_rank = previous_pagerank[search_page]
                    # Pr(i) / Numlink(i)
                    prob_value = pagelink_rank / len(link)
                    # summation
                    sum_value = sum_value + prob_value
            
            prob_from_otherlink = damping_factor*(sum_value)

            # update page rank
            pagerank[page] = constant_prob + prob_from_otherlink

        # check if page rank not change more than 0.001
        count = 0
        for current_pagerank , previous_pagerank in zip(pagerank.values(),previous_pagerank.values()):
            if abs(current_pagerank-previous_pagerank) <= 0.001:
                count+=1
                continue
            else:
                pass
        
        if count == len(pagerank): # Value converge
            break
        else: # continue calcuate next iteration
            previous_pagerank = copy.deepcopy(pagerank)
            continue

    return pagerank


if __name__ == "__main__":
    main()
