from pynini import *

GRAPHEMES = union("'", "-",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I",
                  "J", "K", "L", "M", "N", "N̈", "O", "P", "Q",
                  "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i",
                  "j", "k", "l", "m", "n", "n̈", "o", "p", "q",
                  "r", "s", "t", "u", "v", "w", "x", "y", "z",
                  "À", "Â", "È", "É", "Ê", "Ë", "Ì", "Ò", "Ô", "Ù",
                  "à", "â", "è", "é", "ê", "ë", "ì", "ò", "ô", "ù")

INITIAL_PUMCTUATION = union('"', "'")

FINAL_PUNCTUATION = union("!", '"', ",", ".", ":", ";", "?")
