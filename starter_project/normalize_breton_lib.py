#!/usr/bin/env python
'''Add docstring.'''

from pynini import *

BR_GRAPHEMES = union("a", "b", "c")
HYPHEN = "-"
sigma_star = union(BR_GRAPHEMES, HYPHEN).closure()

DELETE_HYPHEN = transducer(HYPHEN, "")

REMOVE_EXTRA_HYPHEN_IN_WORD = cdrewrite(
  DELETE_HYPHEN,
  BR_GRAPHEMES + pynini.acceptor(HYPHEN),
  BR_GRAPHEMES,
  sigma_star)

def NormalizeBreton(breton_string):
  return breton_string @ REMOVE_EXTRA_HYPHEN_IN_WORD
