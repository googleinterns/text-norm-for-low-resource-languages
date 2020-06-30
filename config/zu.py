from pynini import *

GRAPHEMES = union("'", "-",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I",
                  "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                  "S", "T", "U", "V", "W", "X", "Y", "Z",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i",
                  "j", "k", "l", "m", "n", "o", "p", "q", "r",
                  "s", "t", "u", "v", "w", "x", "y", "z")

INITIAL_PUNCTUATION = union('"', "'")

FINAL_PUNCTUATION = union("!", '"', ",", ".", ":", ";", "?")

HYPHEN = acceptor("-")
SPACE = acceptor(" ")

SIGMA_STAR = union(*("[{}]".format(i) for i in range(1, 256))
                                ).optimize().closure()

NOUN_CLASSIFIERS = union("umu", "um", "u",
                         "aba", "ab", "abe", "o",
                         "umu", "um", "u",
                         "imi", "im",
                         "ili", "i",
                         "ama", "ame",
                         "isi", "is",
                         "izi", "iz",
                         "im", "in", "i",
                         "izim", "izin",
                         "ulu", "u",
                         "ubu", "utsh",
                         "uku", "uk",
                         "uku", "uk").optimize().closure()

LOAN_CLASSIFIER = transducer(HYPHEN, "")

DO_LOAN_CLASSIFIER = cdrewrite(
    LOAN_CLASSIFIER,
    union("[BOS]", SPACE) + NOUN_CLASSIFIERS,
    GRAPHEMES,
    SIGMA_STAR)

LANGUAGE_SPECIFIC_PREPROCESSING = DO_LOAN_CLASSIFIER
