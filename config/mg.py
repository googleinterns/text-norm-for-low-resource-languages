"Malagasy config with language-specific information."

from pynini import *
from config import utils

GRAPHEMES = union("'", "-",
                  "a", "b", "c", "d", "e", "f", "g",
                  "h", "i", "j", "k", "l", "m", "n",
                  "n̈", "ñ", "o", "p", "q", "r", "s",
                  "t", "u", "v", "w", "x", "y", "z",
                  "à", "â", "è", "é", "ê", "ë", "ì", "ò", "ô", "ù")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = utils.WESTERN_ARABIC_NUMERALS

MG_VELAR_NASAL = cdrewrite(
    transducer("ñ", "n̈"),
    "",
    "",
    utils.SIGMA_STAR)

LANGUAGE_SPECIFIC_PREPROCESSING = MG_VELAR_NASAL

UD = ""
UM = ""
AC = "language_data/mg/mg_ac/mg-words.txt"
OSCAR = ""
LCC = "language_data/mg/mlg_wikipedia_2014_30K/mlg_wikipedia_2014_30K-sentences.txt"
#LCC = "language_data/mg/mlg_wikipedia_2014_30K/mlg_web_2012_30K-sentences.txt"
