"Hausa config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-", "ʼ", "ʼ"
                  "ɓ", "ɗ", "ƙ", "ƴ", "r̃")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT


APOSTROPHE_TO_HOOK_Y = cdrewrite(
    cross("ʼy", "ƴ"),
    "",
    "",
    byte.BYTES.closure())

HOOK_TO_APOSTROPHE_Y = cdrewrite(
    cross("ƴ", "ʼy"),
    "",
    "",
    byte.BYTES.closure())

#LANGUAGE_SPECIFIC_PREPROCESSING = APOSTROPHE_TO_HOOK_Y
LANGUAGE_SPECIFIC_PREPROCESSING = HOOK_TO_APOSTROPHE_Y

UD = ""
UM = ""
AC = ""
OSCAR = ""
LCC = ""
