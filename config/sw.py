"Swahili config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

UD = "" # none
UM = ""
AC = "language_data/sw/ac/sw-words.txt"
OSCAR = "language_data/sw/oscar/sw.txt"
OSCAR_DEDUP = "language_data/sw/oscar/sw_dedup.txt"
LCC = "language_data/sw/lcc/swa_wikipedia_2016_100K/swa_wikipedia_2016_100K-sentences.txt"
#LCC = "language_data/sw/lcc/swa_newscrawl_2011_10K/swa_newscrawl_2011_10K-sentences.txt"
#LCC = "language_data/sw/lcc/swh_wikipedia_2011_30K/swh_wikipedia_2011_30K-sentences.txt"
