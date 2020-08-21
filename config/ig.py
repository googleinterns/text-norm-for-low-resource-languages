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

# Converts from the Ọnwụ alphabet to the New Standard Alphabet.
# The New Standard Alphabet is more recent than the Ọnwụ,
# but not frequently used.
TO_NEW_STANDARD_ALPHABET = cdrewrite(
    string_map((
        ("ọ", "ö"),
        ("ụ", "ü"),
        ("ṅ", "ñ"))),
    "",
    "",
    byte.BYTES.closure())

# Converts from the New Standard Alphabet to the Ọnwụ alphabet.
# The Ọnwụ alphabet is slightly older, but more commonly used.
FROM_NEW_STANDARD_ALPHABET = cdrewrite(
    string_map((
        ("ö", "ọ"),
        ("ü", "ụ"),
        ("ñ", "ṅ"))),
    "",
    "",
    byte.BYTES.closure())

#LANGUAGE_SPECIFIC_PREPROCESSING = TO_NEW_STANDARD_ALPHABET
LANGUAGE_SPECIFIC_PREPROCESSING = FROM_NEW_STANDARD_ALPHABET

# These files are not in the repo. You will need to change these paths to match
# where you place the data files.
UD = "" # none
UM = ""
AC = "language_data/ig/ac/ig-wordbigrams.txt"
OSCAR = "" # none
OSCAR_DEDUP = "" # none
LCC = ""
