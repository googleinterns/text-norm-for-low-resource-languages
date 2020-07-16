"Zulu config with language-specific information."

from pynini import *
from config import utils

GRAPHEMES = union(utils.DEFAULT_LATIN, "'", "-",

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = utils.WESTERN_ARABIC_NUMERALS

VOWELS = union("a", "e", "i", "o", "u")

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
