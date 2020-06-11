#!/usr/bin/env python
'''Add docstring.'''

from pynini import *

#BR_GRAPHEMES = union("a", "b", "ch", "c'h", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "v", "w", "y", "z", "D", "G", "K", "'")
BR_GRAPHEMES = union("d", "a", "p", "e", "n", "b", " ")
#SOFT_TRIGGERS = union("da", "dre", "a", "war", "dindan", "eme", "en ur", "pe", "ne", "na", "ez", "ra", "en em", "daou", "div", "pa", "holl", "re", "hini")
SOFT_TRIGGERS = "da"
HARD_TRIGGERS = union("ho", "az", "ez", "d'az")
SPIRANT_TRIGGERS = union("he", "ma", "va", "tri", "teir", "pevar", "peder", "nav")
# Skipping mixed triggers for now, since they are all homographs of triggers
# that trigger other mutations (e.g. "o", "e", and "ma")
#MIXED_TRIGGERS = union("")

HYPHEN = "-"
#sigma_star = union(BR_GRAPHEMES, SOFT_TRIGGERS, HARD_TRIGGERS, SPIRANT_TRIGGERS, HYPHEN).closure()
sigma_star = union(BR_GRAPHEMES, SOFT_TRIGGERS, HYPHEN).closure()

DELETE_HYPHEN = transducer(HYPHEN, "")
#SOFT_MUTATION = string_map((("p", "b"), ("t", "d"), ("k", "g"), ("gw", "w"), ("m", "v")))
SOFT_MUTATION = transducer("p", "b")
#HARD_MUTATION = string_map((("b", "p"), ("d", "t"), ("g", "k"), ("gw", "kw")))
#SPIRANT_MUTATION = string_map((("p", "f"), ("t", "z"), ("k", "c'h")))
# Skipping mixed mutation for now, since all mixed triggers are homographs of
# triggers that trigger another mutation
#MIXED_MUTATION = string_map(("b", "v"), ("d", "t"), ("g", "c'h"), ("gw", "w"), ("m", "v"))

DO_SOFT_MUTATION = cdrewrite(
    SOFT_MUTATION,
    SOFT_TRIGGERS + " ",
    BR_GRAPHEMES,
    sigma_star)

REMOVE_EXTRA_HYPHEN_IN_WORD = cdrewrite(
  DELETE_HYPHEN,
  BR_GRAPHEMES + acceptor(HYPHEN),
  BR_GRAPHEMES,
  sigma_star)

def NormalizeBreton(breton_string):
  return compose(breton_string, REMOVE_EXTRA_HYPHEN_IN_WORD).string()

def NormalizeBretonSoftMutation(breton_string):
  return compose(breton_string, DO_SOFT_MUTATION).string()
