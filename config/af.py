"Afrikaans config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "'", "-",
                  "à", "á", "ä", "è", "é", "ê", "ë",
                  "í", "ï", "ò", "ó", "ô", "ö", "ú", "ü")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

EMBIGGEN_CONTRACTIONS = cdrewrite(
    union(cross("'k", "ek"), cross("'t", "het")),
    union("[BOS]", byte.SPACE),
    union("[EOS]", byte.SPACE),
    byte.BYTES.closure())

LANGUAGE_SPECIFIC_PREPROCESSING = EMBIGGEN_CONTRACTIONS

UD = "language_data/af/UD_Afrikaans-AfriBooms/af_afribooms-ud-train.conllu"
UM = ""
AC = ""
OSCAR = ""
LCC = ""
