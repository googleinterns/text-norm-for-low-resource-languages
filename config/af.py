from pynini import *

GRAPHEMES = union("'", "'", "-",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I",
                  "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                  "S", "T", "U", "V", "W", "X", "Y", "Z",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i",
                  "j", "k", "l", "m", "n", "o", "p", "q", "r",
                  "s", "t", "u", "v", "w", "x", "y", "z",
                  "à", "á", "ä", "è", "é", "ê", "ë",
                  "í", "ï", "ò", "ó", "ô", "ö", "ú", "ü")

INITIAL_PUNCTUATION = union('"', "'")

FINAL_PUNCTUATION = union("!", '"', ",", ".", ":", ";", "?")

SIGMA_STAR = union(*("[{}]".format(i) for i in range(1, 256))
                                ).optimize().closure()

INDEF_ARTICLE = transducer("'n", "<&>")

DO_INDEF_ARTICLE = cdrewrite(
    INDEF_ARTICLE,
    union("[BOS]", " "),
    " ",
    SIGMA_STAR)

LANGUAGE_SPECIFIC_PREPROCESSING = DO_INDEF_ARTICLE
