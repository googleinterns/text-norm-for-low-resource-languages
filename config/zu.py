"Zulu config with language-specific information."

from pynini import *
from pynini.lib import byte, pynutil
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

VOWELS = union("a", "e", "i", "o", "u")

# Some noun classifiers are repeated here, but this table reflects all of the
# different Zulu noun classes. It just so happens that some noun classes use
# homographic noun classifiers.
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

# Normally, Zulu noun classifiers attach directly to the noun (e.g. isiZulu).
# Before nouns beginning with a vowel, which are all loanwords, a hyphen is
# sometimes inserted (e.g. i-Afrika). However, the use of a hyphen is
# inconsistent. This rule removes all hyphens between noun classifiers and words
# beginning with a vowel.
REMOVE_HYPHEN_AFTER_NOUN_CLASSIFIER = cdrewrite(
    pynutil.delete("-"),
    union("[BOS]", byte.SPACE) + NOUN_CLASSIFIERS,
    VOWELS,
    byte.BYTES.closure())

LANGUAGE_SPECIFIC_PREPROCESSING = REMOVE_HYPHEN_AFTER_NOUN_CLASSIFIER

UD = ""
UM = ""
AC = ""
OSCAR = ""
LCC = ""
