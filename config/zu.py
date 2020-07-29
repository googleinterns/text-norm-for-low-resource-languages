"Zulu config with language-specific information."

from pynini import *
from pynini.lib import byte, pynutil
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

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
    pynutil.delete("-"),
    union("[BOS]", byte.SPACE) + NOUN_CLASSIFIERS,
    VOWELS,
    byte.BYTES.closure())

LANGUAGE_SPECIFIC_PREPROCESSING = REMOVE_HYPHEN_AFTER_NOUN_CLASSIFIER

UD = "" # none
UM = "language_data/zu/zu_um.txt"
AC = "language_data/zu/ac/zu-words.txt"
OSCAR = "" # none
OSCAR_DEDUP = "" # none
LCC = "language_data/zu/lcc/zul_mixed_2014_100K/zul_mixed_2014_100K-sentences.txt"
#LCC = "language_data/zu/lcc/zul_news_2013_30K/zul_news_2013_30K-sentences.txt"
#LCC = "language_data/zu/lcc/zul_web_2013_100K/zul_web_2013_100K-sentences.txt"
#LCC = "language_data/zu/lcc/zul-za_web_2018_30K/zul-za_web_2018_30K-sentences.txt"
