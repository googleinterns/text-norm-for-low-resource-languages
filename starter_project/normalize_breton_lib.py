#!/usr/bin/env python
'''Add docstring.'''

from pynini import *
import re

# add more graphemes for French (and other language) names/words in the texts?
# more punctuation?
BR_GRAPHEMES = union(
    "a", "b", "ch", "c'h", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "v", "w", "y", "z", "c",
    "A", "B", "CH", "C'H", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "W", "Y", "Z", "C",
    "â", "ê", "ô", "ù", "ü", "ñ",
    "Â", "Ê", "Ô", "Ù", "Ü", "Ñ",
    "'", " ")

SOFT_TRIGGERS = union("da", "dre", "a", "war", "dindan", "eme", "en ur", "pe", "ne", "na", "ez", "ra", "en em", "daou", "div", "pa", "holl", "re", "hini"
                      #"e", "tra",
                      )

HARD_TRIGGERS = union("ho", "az", "ez", "da'z")

SPIRANT_TRIGGERS = union("he", "ma", "va", "tri", "teir", "pevar", "peder", "nav", "hon"
                         #"o"
                         )

# Skipping mixed triggers for now, since they are all homographs of triggers
# that trigger other mutations (e.g. "o", "e", and "ma")
#MIXED_TRIGGERS = union("o", "e", "ma")

HYPHEN = "-"
SPACE = " "
WORD_BOUNDARY = "\b"
#WORD_BOUNDARY = ""
sigma_star = union(BR_GRAPHEMES, SOFT_TRIGGERS, HARD_TRIGGERS, SPIRANT_TRIGGERS, SPACE, HYPHEN, WORD_BOUNDARY).closure()

DELETE_HYPHEN = transducer(HYPHEN, "")

SOFT_MUTATION = string_map((
    ("p", "b"), ("P", "B"),
    ("t", "d"), ("T", "D"),
    ("k", "g"), ("K", "G"),
    ("gw", "w"), ("Gw", "W"), ("GW", "W"),
    ("m", "v"), ("M", "V")))

HARD_MUTATION = union(
    transducer("b", "p"),
    transducer("d", "t"),
    transducer("g", "k"),
    transducer("gw", "kw", -1),
    transducer("Gw", "Kw", -1),
    transducer("GW", "KW", -1),
    transducer("m", "v"))

SPIRANT_MUTATION = string_map((
    ("p", "f"), ("P", "F"),
    ("t", "z"), ("T", "Z"),
    ("k", "c'h"), ("K", "C'h")))

# Skipping mixed mutation for now, since all mixed triggers are homographs of
# triggers that trigger another mutation
#MIXED_MUTATION = string_map(("b", "v"), ("d", "t"), ("g", "c'h"), ("gw", "w"), ("m", "v"))

DO_SOFT_MUTATION = cdrewrite(
    SOFT_MUTATION,
    SOFT_TRIGGERS + acceptor(SPACE),
    BR_GRAPHEMES,
    sigma_star)

DO_HARD_MUTATION = cdrewrite(
    HARD_MUTATION,
    HARD_TRIGGERS + acceptor(SPACE),
    BR_GRAPHEMES,
    sigma_star)

DO_SPIRANT_MUTATION = cdrewrite(
    SPIRANT_MUTATION,
    SPIRANT_TRIGGERS + acceptor(SPACE),
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

def NormalizeBretonHardMutation(breton_string):
  return compose(breton_string, DO_HARD_MUTATION).string()

def NormalizeBretonSpirantMutation(breton_string):
  return compose(breton_string, DO_SPIRANT_MUTATION).string()

