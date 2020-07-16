"Afrikaans config with language-specific information."

from pynini import *
from config import utils

GRAPHEMES = union("'", "'", "-",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i",
                  "j", "k", "l", "m", "n", "o", "p", "q", "r",
                  "s", "t", "u", "v", "w", "x", "y", "z",
                  "à", "á", "ä", "è", "é", "ê", "ë",
                  "í", "ï", "ò", "ó", "ô", "ö", "ú", "ü")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = utils.WESTERN_ARABIC_NUMERALS

AF_INDEF_ARTICLE = cdrewrite(
    transducer("'n", "<&>"),
    union("[BOS]", " "),
    " ",
    utils.SIGMA_STAR)

LANGUAGE_SPECIFIC_PREPROCESSING = AF_INDEF_ARTICLE

UD = "language_data/af/UD_Afrikaans-AfriBooms/af_afribooms-ud-train.conllu"
UM = ""
AC = ""
OSCAR = ""
LCC = ""
