"Yoruba config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-",
                  "à", "á", "è", "é", "ì", "í", "ò", "ó", "ù", "ú",
                  "ṣ", "ẹ", "ẹ̀", "ẹ́", "ọ", "ọ̀", "ọ́")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

UD = ""
UM = ""
AC = ""
OSCAR = ""
LCC = ""
