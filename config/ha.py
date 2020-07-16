"Hausa config with language-specific information."

from pynini import *
from config import utils

GRAPHEMES = union(utils.DEFAULT_LATIN, "'", "-", "ʼ"
                  "ɓ", "ɗ", "ƙ", "ƴ", "r̃")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = utils.WESTERN_ARABIC_NUMERALS

UD = ""
UM = ""
AC = ""
OSCAR = ""
LCC = ""
