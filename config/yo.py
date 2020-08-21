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

UD = "language_data/yo/UD_Yoruba-YTB/yo_ytb-ud-test.conllu"
UM = ""
AC = "language_data/yo/ac/yo-wordbigrams.txt"
OSCAR = "language_data/yo/oscar/yo.txt"
OSCAR_DEDUP = "language_data/yo/oscar/yo_dedup.txt"
LCC = "language_data/yo/lcc/yor_wikipedia_2016_10K/yor_wikipedia_2016_10K-sentences.txt"
