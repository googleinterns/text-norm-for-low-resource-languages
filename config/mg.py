"Malagasy config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-", "@",
                  "à", "â", "è", "é", "ê", "ë",
                  "ì", "ò", "ô", "ù", "n̈", "ñ")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

# Malagasy's official orthography uses n with diaeresis, but many keyboards do
# not have this grapheme, so users often replace it with n with tilde. This rule
# normalizes the text towards the official orthography.
MG_VELAR_NASAL = cdrewrite(
    cross("ñ", "n̈"),
    "",
    "",
    byte.BYTES.closure())

# Malagasy speakers apparently use <@> as an abbreviation for <amin'ny>, meaning
# 'with the'. This rule transduces standalone <@> back into <amin'ny>.
MG_ABBREVIATION = cdrewrite(
    cross("@", "amin'ny"),
    union("[BOS]", byte.SPACE),
    union("[EOS]", byte.SPACE),
    byte.BYTES.closure())

LANGUAGE_SPECIFIC_PREPROCESSING = (MG_VELAR_NASAL @ MG_ABBREVIATION).optimize()

UD = ""
UM = ""
AC = "language_data/mg/ac/mg-wordbigrams.txt"
OSCAR = "language_data/mg/oscar/mg.txt"
OSCAR_DEDUP = "language_data/mg/oscar/mg_dedup.txt"
LCC = "language_data/mg/lcc/mlg_wikipedia_2014_30K/mlg_wikipedia_2014_30K-sentences.txt"
#LCC = "language_data/mg/lcc/mlg_web_2012_30K/mlg_web_2012_30K-sentences.txt"
