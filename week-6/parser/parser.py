import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP | VP | S Conj S

NP -> N | Det N | AP NP | N PP | NP Conj NP
VP -> V | V NP | V PP | V NP PP
AP -> Adj | Adj AP | Det AP
PP -> P NP | P AP 
"""

# S -> N Adv V Det N Conj N V P Det N Adv
# S -> [NP] [Adv] [VP] [NP] [Conj] [NP] [VP] [PP] [Adv]
# S -> [NP] [Adv] [VP] [NP] [VP] [PP] [Adv]
# S -> [NP] [ADVP] [NP] [VP] [ADVP]
#

# S -> N V Adv Conj V Det N
# S -> [NP] [VP] [Adv] [Conj] [NP]
# S -> [NP] [ADVP] [Conj] [NP]
ALTTERMINALS = """
S -> NP VP | NP | VP | NP ADVP | S Conj S

NP -> N | Det N | AP NP | N PP | NP Conj NP
VP -> V | V NP | V PP | V NP PP
AP -> Adj | Adj AP | Det AP
PP -> P NP | P AP
ADVP -> VP Adv | Adv VP | PP Adv
"""

grammar = nltk.CFG.fromstring(ALTTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    return [
        word.lower() for word in nltk.word_tokenize(sentence) if word != "."
    ]


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
