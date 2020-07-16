"Bambara config with language-specific information."

from pynini import *
from config import utils

GRAPHEMES = union("'", "-",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I",
                  "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                  "S", "T", "U", "V", "W", "X", "Y", "Z",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i",
                  "j", "k", "l", "m", "n", "o", "p", "q", "r",
                  "s", "t", "u", "v", "w", "x", "y", "z",
                  "À", "Â", "Æ", "Ç", "È", "É", "Ê", "Ë",
                  "Ì", "Î", "Ï", "Ò", "Ô", "Ù", "Û", "Ü",
                  "à", "â", "æ", "ç", "è", "é", "ê", "ë",
                  "ì", "î", "ï", "ò", "ô", "ù", "û", "ü",
                  "Ŋ", "ŋ", "Œ", "œ", "Ɔ", "Ɛ", "Ɲ", "ɔ", "ɛ", "ɲ")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = utils.WESTERN_ARABIC_NUMERALS

UD = ""
UM = ""
AC = ""
OSCAR = ""
LCC = ""
