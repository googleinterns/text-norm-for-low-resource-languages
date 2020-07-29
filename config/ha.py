"Hausa config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-", "ʼ"
                  "ɓ", "ɗ", "ƙ", "ƴ", "r̃")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

UD = "" # none
UM = ""
AC = "language_data/ha/ac/ha-words.txt"
OSCAR = "" # none
OSCAR_DEDUP = "" # none
LCC = ""
