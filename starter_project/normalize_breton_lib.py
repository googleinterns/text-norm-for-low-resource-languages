#!/usr/bin/env python
'''Add docstring.'''

from pynini import *

BR_GRAPHEMES = union("a", "b", "ch", "c'h", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "v", "w", "y", "z")
SOFT_TRIGGERS = union("da", "dre", "a", "war", "dindan", "eme", "en ur", "pe", "ne", "na", "ez", "ra", "en em", "daou", "div", "pa", "holl", "re", "hini")
HARD_TRIGGERS = union("ho", "az", "ez", "d'az")
SPIRANT_TRIGGERS = union("he", "ma", "va", "tri", "teir", "pevar", "peder", "nav")
#MIXED_TRIGGERS = union("")

HYPHEN = "-"
sigma_star = union(BR_GRAPHEMES, HYPHEN).closure()

DELETE_HYPHEN = transducer(HYPHEN, "")
SOFT_MUTATION = string_map(("p", "b"), ("t", "d"), ("k", "g"), ("gw", "w"), ("m", "v"))
HARD_MUTATION = string_map(("b", "p"), ("d", "t"), ("g", ("k"), ("gw", "kw"))
SPIRANT_MUTATION = string_map(("p", "f"), ("t", "z"), ("k", "c'h"))
#MIXED_MUTATION = string_map(("b", "v"), ("d", "t"), ("g", "c'h"), ("gw", "w"), ("m", "v"))

REMOVE_EXTRA_HYPHEN_IN_WORD = cdrewrite(
  DELETE_HYPHEN,
  BR_GRAPHEMES + acceptor(HYPHEN),
  BR_GRAPHEMES,
  sigma_star)

def NormalizeBreton(breton_string):
  return compose(breton_string, REMOVE_EXTRA_HYPHEN_IN_WORD).string()
