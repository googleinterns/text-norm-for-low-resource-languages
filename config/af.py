"Afrikaans config with language-specific information."

from pynini import *
from config import utils

GRAPHEMES = union(utils.DEFAULT_LATIN, "'", "'", "-",
                  "à", "á", "ä", "è", "é", "ê", "ë",
                  "í", "ï", "ò", "ó", "ô", "ö", "ú", "ü")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = utils.WESTERN_ARABIC_NUMERALS

UD = "language_data/af/UD_Afrikaans-AfriBooms/af_afribooms-ud-train.conllu"
UM = ""
AC = ""
OSCAR = ""
LCC = ""
