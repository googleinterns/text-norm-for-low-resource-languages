from pynini import *

GRAPHEMES=union("'", "-",
                "A", "B", "C", "D", "E", "F", "G", "H", "I",
                "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                "S", "T", "U", "V", "W", "X", "Y", "Z",
                "a", "b", "c", "d", "e", "f", "g", "h", "i",
                "j", "k", "l", "m", "n", "o", "p", "q", "r",
                "s", "t", "u", "v", "w", "x", "y", "z")

INITIAL_PUNCTUATION=union('"', "'")

FINAL_PUNCTUATION=union("!", '"', ",", ".", ":", ";", "?")

NUMBERS = union("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

ud = ""
um = ""
ac = ""
oscar = ""
lcc = ""
