"Hausa config with language-specific information."

from pynini import *
from config import utils

GRAPHEMES = union("'", "-", "ʼ"
                  "A", "B", "C", "D", "E", "F", "G", "H", "I",
                  "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                  "S", "T", "U", "V", "W", "X", "Y", "Z",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i",
                  "j", "k", "l", "m", "n", "o", "p", "q", "r",
                  "s", "t", "u", "v", "w", "x", "y", "z",
                  "Ɓ", "Ɗ", "Ƙ", "Ƙ", "R̃",
                  "ɓ", "ɗ", "ƙ", "ƴ", "r̃")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = utils.WESTERN_ARABIC_NUMERALS

UD = ""
UM = ""
AC = ""
OSCAR = ""
LCC = ""
