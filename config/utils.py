# Lint as: python3
"Config for language-independent sets of graphemes, symbols, etc."

from pynini import *

DEFAULT_INITIAL_PUNCTUATION = union("\"", "'")
DEFAULT_FINAL_PUNCTUATION = union("!", "\"", ",", ".", ":", ";", "?")

SIGMA_STAR = union(*("[{}]".format(i) for i in range(1, 256))
                   ).optimize().closure()
