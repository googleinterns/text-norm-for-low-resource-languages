"Wolof config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-",
                  "à", "á", "â", "ã", "ä", "å", "æ", "ç",
                  "è", "é", "ê", "ë", "í", "î", "ï", "ñ",
                  "ò", "ó", "ô", "ö", "ø", "ù", "ú", "û", "ü",
                  "ā", "ă", "ć", "ĉ", "č", "đ", "ĝ", "ĥ", "ī", "ı",
                  "ĵ", "ł", "ŋ", "ō", "œ", "ś", "ŝ", "š", "ū", "ŭ",
                  "ž", "ɓ", "ɗ", "ɲ", "ḍ", "ḥ", "ṣ", "ṭ", "ẓ")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

UD = ""
UM = ""
AC = ""
OSCAR = ""
LCC = ""
