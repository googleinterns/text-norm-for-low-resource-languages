"Bambara config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-",
                  "à", "â", "æ", "ç", "è", "é", "ê", "ë",
                  "ì", "î", "ï", "ò", "ô", "ù", "û", "ü",
                  "ŋ", "œ", "ɔ", "ɛ", "ɲ")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

# These files are not in the repo. You will need to change these paths to match
# where you place the data files.
UD = "language_data/bm_latn/UD_Bambara-CRB/bm_crb-ud-test.conllu"
UM = ""
AC = "language_data/bm_latn/ac/bm-wordbigrams.txt"
OSCAR = "" # none
OSCAR_DEDUP = "" # none
LCC = ""
