"Somali config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

# These files are not in the repo. You will need to change these paths to match
# where you place the data files.
UD = "" # none
UM = ""
AC = "language_data/so/ac/so-words.txt"
OSCAR = "language_data/so/oscar/so.txt"
OSCAR_DEDUP = "language_data/so/oscar/so_dedup.txt"
#LCC = "language_data/so/lcc/som_newscrawl_2011_100K/som_newscrawl_2011_100K-sentences.txt"
LCC = "language_data/so/lcc/som_wikipedia_2016_10K/som_wikipedia_2016_10K-sentences.txt"
