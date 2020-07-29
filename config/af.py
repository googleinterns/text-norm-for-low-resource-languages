"Afrikaans config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "'", "-",
                  "à", "á", "ä", "è", "é", "ê", "ë",
                  "í", "ï", "ò", "ó", "ô", "ö", "ú", "ü")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

UD = "language_data/af/UD_Afrikaans-AfriBooms/af_afribooms-ud-train.conllu"
UM = ""
AC = "language_data/af/ac/af-words.txt"
OSCAR = "language_data/af/oscar/af.txt"
OSCAR_DEDUP = "language_data/af/oscar/af_dedup.txt"
LCC = "language_data/af/lcc/afr_mixed_2019_1M/afr_mixed_2019_1M-sentences.txt"
