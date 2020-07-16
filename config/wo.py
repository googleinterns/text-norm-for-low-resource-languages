"Wolof config with language-specific information."

from pynini import *
from config import utils

GRAPHEMES = union("'", "-",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I",
                  "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                  "S", "T", "U", "V", "W", "X", "Y", "Z",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i",
                  "j", "k", "l", "m", "n", "o", "p", "q", "r",
                  "s", "t", "u", "v", "w", "x", "y", "z",
                  "à", "á", "â", "ã", "ä", "å", "æ", "ç",
                  "è", "é", "ê", "ë", "í", "î", "ï", "ñ",
                  "ò", "ó", "ô", "ö", "ø", "ù", "ú", "û", "ü",
                  "ā", "ă", "ć", "ĉ", "č", "đ", "ĝ", "ĥ", "ī", "ı",
                  "ĵ", "ł", "ŋ", "ō", "œ", "ś", "ŝ", "š", "ū", "ŭ",
                  "ž", "ɓ", "ɗ", "ɲ", "ḍ", "ḥ", "ṣ", "ṭ", "ẓ")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = utils.WESTERN_ARABIC_NUMERALS

UD = ""
UM = ""
AC = ""
OSCAR = ""
LCC = ""
