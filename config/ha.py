"Hausa config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-", "ʼ", "ʼ"
                  "ɓ", "ɗ", "ƙ", "ƴ", "r̃")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

# Hausa in Niger uses y with right hook. This rule converts modifier letter
# apostrophe y (used in Nigeria) to the Niger standard.
APOSTROPHE_TO_HOOK_Y = cdrewrite(
    cross("'y", "ƴ"),
    "",
    "",
    byte.BYTES.closure())

# Hausa in Nigeria uses modifier letter apostrophe y. This rule converts y with
# right hook (used in Niger) to the Nigeria standard.
HOOK_TO_APOSTROPHE_Y = cdrewrite(
    cross("ƴ", "ʼy"),
    "",
    "",
    byte.BYTES.closure())

LANGUAGE_SPECIFIC_PREPROCESSING = APOSTROPHE_TO_HOOK_Y
#LANGUAGE_SPECIFIC_PREPROCESSING = HOOK_TO_APOSTROPHE_Y

# These files are not in the repo. You will need to change these paths to match
# where you place the data files.
UD = "" # none
UM = ""
AC = "language_data/ha/ac/ha-wordbigrams.txt"
OSCAR = "" # none
OSCAR_DEDUP = "" # none
LCC = ""
