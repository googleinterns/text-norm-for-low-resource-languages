#!/usr/bin/env python
"""Library of language-agnostic FST rewrite rules to normalize text."""

from pynini import *

# temporary placeholder, will load language-specific graphemes from config
GRAPHEMES = union("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"
                  "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                  "Y", "Z",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                  "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
                  "y", "z")

SPACE = acceptor(" ")

SIGMA_STAR = union(*("[{}]".format(i) for i in range(1, 256))).optimize().closure()


# Step 1: Remove all extra whitespace between words
# e.g. "hi     there" -> "hi there"

REMOVE_EXTRA_WHITESPACE = transducer(SPACE.plus, SPACE)

DO_REMOVE_EXTRA_WHITESPACE = cdrewrite(
    REMOVE_EXTRA_WHITESPACE,
    GRAPHEMES,
    GRAPHEMES,
    SIGMA_STAR)


def normalize_everything(string: str) -> str:
    "Apply language-agnostic rewrite rules."
    return (string @ DO_REMOVE_EXTRA_WHITESPACE).string()