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

# Afrikaans <ek> and <het> are often contracted to <'k> and <'t>.
# This rule expands the contractions to their full forms.
EMBIGGEN_CONTRACTIONS = cdrewrite(
    string_map((("'k", "ek"),
                ("'t", "het"))),
    union("[BOS]", byte.SPACE),
    union("[EOS]", byte.SPACE),
    byte.BYTES.closure())

LANGUAGE_SPECIFIC_PREPROCESSING = EMBIGGEN_CONTRACTIONS

# These files are not in the repo. You will need to change these paths to match
# where you place the data files.
UD = "language_data/af/UD_Afrikaans-AfriBooms/af_afribooms-ud-train.conllu"
UM = ""
AC = "language_data/af/ac/af-wordbigrams.txt"
OSCAR = "language_data/af/oscar/af.txt"
OSCAR_DEDUP = "language_data/af/oscar/af_dedup.txt"
#LCC = "language_data/af/lcc/afr_mixed_2019_1M/afr_mixed_2019_1M-sentences.txt"
#LCC = "language_data/af/lcc/afr_mixed_2019_300K/afr_mixed_2019_300K-sentences.txt"
#LCC = "language_data/af/lcc/afr_mixed_2019_100K/afr_mixed_2019_100K-sentences.txt"
LCC = "language_data/af/lcc/afr_mixed_2019_30K/afr_mixed_2019_30K-sentences.txt"
#LCC = "language_data/af/lcc/afr_mixed_2019_1M/afr_mixed_2019_10K-sentences.txt"
