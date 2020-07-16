"Zulu config with language-specific information."

from pynini import *
from config import utils

GRAPHEMES = union("'", "-",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I",
                  "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                  "S", "T", "U", "V", "W", "X", "Y", "Z",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i",
                  "j", "k", "l", "m", "n", "o", "p", "q", "r",
                  "s", "t", "u", "v", "w", "x", "y", "z")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = utils.WESTERN_ARABIC_NUMERALS

VOWELS = union("A", "E", "I", "O", "U",
               "a", "e", "i", "o", "u")

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

REMOVE_HYPHEN_AFTER_NOUN_CLASSIFIER = cdrewrite(
    transducer("-", ""),
    union("[BOS]", " ") + NOUN_CLASSIFIERS,
    VOWELS,
    utils.SIGMA_STAR)

LANGUAGE_SPECIFIC_PREPROCESSING = REMOVE_HYPHEN_AFTER_NOUN_CLASSIFIER

UD = ""
UM = ""
AC = ""
OSCAR = ""
LCC = ""
