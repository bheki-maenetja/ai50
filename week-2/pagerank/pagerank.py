from hashlib import new
import os
import random
import re
import sys

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
    linked_pages = corpus[page]
    num_linked_pages = len(linked_pages) if len(linked_pages) != 0 else len(corpus)
    new_damping_factor = round(damping_factor / num_linked_pages, 5)
    non_damping_factor = round((1 - damping_factor) / (num_linked_pages + 1), 5)
    transition_model = { page : non_damping_factor }
    transition_model.update({ linked_page : non_damping_factor + new_damping_factor for linked_page in linked_pages })
    return transition_model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    start_page = random.choice(list(corpus.keys()))
    new_model = transition_model(corpus, start_page, damping_factor)
    
    markov_chain = []
    for i in range(n):
        new_page = random.choices(list(new_model.keys()), weights=list(new_model.values()))[0]
        markov_chain.append(new_page)
        new_model = transition_model(corpus, new_page, damping_factor)
    
    page_rank_dict = { key : round(markov_chain.count(key) / n, 5) for key in corpus.keys() }
    return page_rank_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    non_damping_factor = 1 - damping_factor
    num_pages = len(corpus)

    page_rank_dict = { key: 1/num_pages for key in corpus }
    new_and_prev_ranks = { key: (page_rank_dict[key], 0) for key in page_rank_dict }

    while not all(abs(tup[0] - tup[1]) < 0.001 for tup in new_and_prev_ranks.values()):
        for page in page_rank_dict:
            current_rank = page_rank_dict[page]
            new_rank = (non_damping_factor / num_pages)
            for linked_page in corpus[page]:
                num_links = len(corpus[linked_page]) if len(corpus[linked_page]) != 0 else len(corpus)
                new_rank += damping_factor * page_rank_dict[linked_page] / num_links
            page_rank_dict[page] = new_rank
            new_and_prev_ranks[page] = (current_rank, new_rank)
    
    return page_rank_dict

if __name__ == "__main__":
    main()
