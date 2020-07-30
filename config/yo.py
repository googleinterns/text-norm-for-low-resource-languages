"Yoruba config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-",
                  "á", "à", "ā",
                  "é", "è", "ē", "ẹ", "e̩",
                  "ẹ́", "é̩", "ẹ̀", "è̩", "ē̩", "ẹ̄",
                  "í", "ì", "ī",
                  "ó", "ò", "ō", "ọ", "o̩",
                  "ọ́", "ó̩", "ọ̀", "ò̩", "ō̩", "ọ̄",
                  "ú", "ù", "ū",
                  "ṣ", "s̩",
                  "n̄", "ń", "ǹ", "ḿ",
                  "ɛ", "ɔ")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

UD = ""
UM = ""
AC = ""
OSCAR = ""
LCC = ""
