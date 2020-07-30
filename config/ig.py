"Igbo config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union(byte.LOWER, "'", "-",
                  "à", "â", "æ", "ç", "è", "é", "ê", "ë",
                  "ì", "î", "ï", "ò", "ô", "ù", "û", "ü",
                  "ị", "ň", "ñ", "ṅ", "ọ", "ụ", "ö")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = utils.DEFAULT_FINAL_PUNCTUATION

NUMERALS = byte.DIGIT

TO_NEW_STANDARD_ALPHABET = cdrewrite(
    union(cross("ọ", "ö"), cross("ụ", "ü"), cross("ṅ", "ñ")),
    "",
    "",
    byte.BYTES.closure())

FROM_NEW_STANDARD_ALPHABET = cdrewrite(
    union(cross("ö", "ọ"), cross("ü", "ụ"), cross("ñ", "ṅ")),
    "",
    "",
    byte.BYTES.closure())

LANGUAGE_SPECIFIC_PREPROCESSING = FROM_NEW_STANDARD_ALPHABET

UD = ""
UM = ""
AC = ""
OSCAR = ""
LCC = ""
