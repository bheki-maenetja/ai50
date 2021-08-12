import nltk
import sys
import os
from string import punctuation
from math import log1p

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
    main_path = os.path.join(os.path.dirname(__file__), directory)
    file_dict = dict()

    for file in os.listdir(main_path):
        with open(os.path.join(main_path, file), 'r') as f:
            file_dict[file] = f.read()
    
    return file_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    banned = list(punctuation) + nltk.corpus.stopwords.words("english")

    return [
        word.lower() for word in nltk.word_tokenize(document)
        if word.lower() not in banned
    ]

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    file_idfs = dict()
    unique_words = set()

    total_docs = len(documents)

    for doc in documents:
        unique_words = set().union(unique_words, set(documents[doc]))
    
    for word in unique_words:
        num_appearances = sum(
            1 for doc in documents 
            if word in documents[doc]
        )
        file_idfs[word] = log1p(total_docs / num_appearances)
    
    return file_idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf_scores = { file: 0 for file in files }

    for word in query:
        for file in files:
            tf = files[file].count(word)
            idf = idfs.get(word)
            tf_idf_scores[file] += tf * idf
    
    ranked_files = sorted(
        tf_idf_scores.items(), 
        key=lambda x: x[1], 
        reverse=True
    )

    return [file[0] for file in ranked_files][:n]     


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_scores = { sent: [0, 0] for sent in sentences }
    
    for sent in sentences:
        common_words = query.intersection(set(sentences[sent]))
        sentence_scores[sent][1] = len(common_words)
        for word in common_words:
            sentence_scores[sent][0] += idfs.get(word)
    
    ranked_sents = sorted(
        sentence_scores.items(),
        key=lambda x: (x[1][0], x[1][1]),
        reverse=True
    )

    for sent in ranked_sents:
        print(sent)
    return [sent[0] for sent in ranked_sents][:n]


if __name__ == "__main__":
    main()
