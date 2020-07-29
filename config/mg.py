"Malagasy config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-",
                  "à", "â", "è", "é", "ê", "ë",
                  "ì", "ò", "ô", "ù", "n̈", "ñ")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

MG_VELAR_NASAL = cdrewrite(
    cross("ñ", "n̈"),
    "",
    "",
    byte.BYTES.closure())

LANGUAGE_SPECIFIC_PREPROCESSING = MG_VELAR_NASAL

UD = ""
UM = ""
AC = "language_data/mg/ac/mg-words.txt"
OSCAR = "language_data/mg/oscar/mg.txt"
OSCAR_DEDUP = "language_data/mg/oscar/mg_dedup.txt"
#LCC = "language_data/mg/lcc/mlg_wikipedia_2014_30K/mlg_wikipedia_2014_30K-sentences.txt"
LCC = "language_data/mg/lcc/mlg_web_2012_30K/mlg_web_2012_30K-sentences.txt"
