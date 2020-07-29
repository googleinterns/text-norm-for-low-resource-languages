"Igbo config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-",
                  "à", "â", "æ", "ç", "è", "é", "ê", "ë",
                  "ì", "î", "ï", "ò", "ô", "ù", "û", "ü",
                  "ị", "ň", "ñ", "ṅ", "ọ", "ụ")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

UD = "" # none
UM = ""
AC = "language_data/ig/ac/ig-words.txt"
OSCAR = "" # none
OSCAR_DEDUP = "" # none
LCC = ""
