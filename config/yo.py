"Yoruba config with language-specific information."

from pynini import *
from config import utils

GRAPHEMES = union("'", "-",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I",
                  "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                  "S", "T", "U", "V", "W", "X", "Y", "Z",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i",
                  "j", "k", "l", "m", "n", "o", "p", "q", "r",
                  "s", "t", "u", "v", "w", "x", "y", "z",
                  "À", "Á", "È", "É", "Ì", "Í", "Ò", "Ó", "Ù", "Ú",
                  "à", "á", "è", "é", "ì", "í", "ò", "ó", "ù", "ú",
                  "Ṣ", "ṣ", "Ẹ", "Ẹ̀", "Ẹ́", "ẹ", "ẹ̀", "ẹ́",
                  "Ọ", "Ọ̀", "Ọ́", "ọ", "ọ̀", "ọ́")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = utils.WESTERN_ARABIC_NUMERALS

UD = ""
UM = ""
AC = ""
OSCAR = ""
LCC = ""
