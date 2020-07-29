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

UD = "language_data/yo/UD_Yoruba-YTB/yo_ytb-ud-test.conllu" # not found for some reason
UM = ""
AC = "language_data/yo/ac/yo-words.txt"
OSCAR = "language_data/yo/oscar/yo.txt"
OSCAR_DEDUP = "language_data/yo/oscar/yo_dedup.txt"
LCC = "language_data/yo/lcc/yor_wikipedia_2016_10K/yor_wikipedia_2016_10K-sentences.txt"
