# Lint as: python3
"Config for language-independent sets of graphemes, symbols, etc."

from pynini import *

DEFAULT_INITIAL_PUNCTUATION = union("\"", "'")
DEFAULT_FINAL_PUNCTUATION = union("!", "\"", ",", ".", ":", ";", "?")
GEEZ_FINAL_PUNCTUATION = union("፠", "፡", "።", "፣", "፤",
                               "፥", "፦", "፧", "፨")
GEEZ_NUMERALS = union("፩", "፪", "፫", "፬", "፭",
                      "፮", "፯", "፰", "፱", "፲",
                      "፳", "፴", "፵", "፶", "፷",
                      "፸", "፹", "፺", "፻",
                      "፲፻", "፻፻", "፲፻፻")
