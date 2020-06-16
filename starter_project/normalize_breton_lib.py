#!/usr/bin/env python
'''Add docstring.'''

from pynini import *
#import re

BR_GRAPHEMES = union(
    "a", "b", "ch", "c'h", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "v", "w", "y", "z",
#    "â", "à", "â", "à", "æ", "ç", "é", "è", "ê", "ë", "ï", "î", "ô", "œ", "ù", "û", "ü", "ÿ", "ê", "ô", "ù", "ü", "ñ",
    "â", "ê", "î", "ô", "û", "ù", "ü", "ñ",
#    "'", "-", "’", " ",
#    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    )

SOFT_TRIGGERS = union("da", "dre", "a", "war", "dindan", "eme", "en ur", "ne", "na", "ez", "ra", "en em", "daou", "div", "pa", "pe", "an holl", "re",
                      #"hini"
                      #"e", "tra",
                      )

HARD_TRIGGERS = union("ho", "az", "ez", "da'z")

SPIRANT_TRIGGERS = union("he", "va", "tri", "teir", "pevar", "peder", "nav", "hon"
                         #"ma", "o"
                         )

# Skipping mixed triggers for now, since they are all homographs of triggers
# that trigger other mutations (e.g. "o", "e", and "ma")
#MIXED_TRIGGERS = union("o", "e", "ma")

SPACE = " "
UNICODE = union(*("[{}]".format(i) for i in range(1, 256))).optimize()
sigma_star = union(BR_GRAPHEMES, SOFT_TRIGGERS, HARD_TRIGGERS, SPIRANT_TRIGGERS, SPACE, UNICODE).closure()

SOFT_MUTATION = string_map((
    ("p", "b"),
    ("t", "d"),
    ("k", "g"),
    ("gw", "w"),
    ("m", "v")
    ))

HARD_MUTATION = union(
    transducer("b", "p"),
    transducer("d", "t"),
    transducer("g", "k"),
    transducer("gw", "kw", -1), # remove because g -> k already exists?
    transducer("m", "v")
    )

SPIRANT_MUTATION = string_map((
    ("p", "f"),
    ("t", "z"),
    ("k", "c'h")
    ))

PREPROCESS = union(
    transducer("a ra", "aaaaara") # TODO: do this better
    )

POSTPROCESS = union(
    transducer("aaaaara", "a ra"),
    transducer("dre va", "dre ma")
    )

# Skipping mixed mutation for now, since all mixed triggers are homographs of
# triggers that trigger another mutation
#MIXED_MUTATION = union(
#    transducer("b", "v"),
#    transducer("d", "t"),
#    transducer("g", "c'h"),
#    transducer("gw", "w", -1),
#    transducer("m", "v")
#    )

DO_SOFT_MUTATION = cdrewrite(
    SOFT_MUTATION,
    union(SPACE, "[BOS]") + SOFT_TRIGGERS + acceptor(SPACE),
    BR_GRAPHEMES,
    sigma_star)

DO_HARD_MUTATION = cdrewrite(
    HARD_MUTATION,
    union(SPACE, "[BOS]") + HARD_TRIGGERS + acceptor(SPACE),
    BR_GRAPHEMES,
    sigma_star)

DO_SPIRANT_MUTATION = cdrewrite(
    SPIRANT_MUTATION,
    union(SPACE, "[BOS]") + SPIRANT_TRIGGERS + acceptor(SPACE),
    BR_GRAPHEMES,
    sigma_star)

DO_PREPROCESSING = cdrewrite(
    PREPROCESS,
    union(SPACE, "[BOS]"),
    union(BR_GRAPHEMES, SPACE),
    sigma_star)

DO_POSTPROCESSING = cdrewrite(
    POSTPROCESS,
    union(SPACE, "[BOS]"),
    union(BR_GRAPHEMES, SPACE),
    sigma_star)


def NormalizeBretonSoftMutation(breton_string: str) -> str:
  """Apply the Breton soft mutation."""
  preprocess_string = compose(breton_string.strip().lower(), DO_PREPROCESSING).string()
  apply_mutation = compose(preprocess_string, DO_SOFT_MUTATION).string()
  postprocess_string = compose(apply_mutation, DO_POSTPROCESSING).string()
  return postprocess_string


def NormalizeBretonHardMutation(breton_string: str) -> str:
  """Apply the Breton hard mutation."""
  preprocess_string = compose(breton_string.strip().lower(), DO_PREPROCESSING).string()
  apply_mutation = compose(preprocess_string, DO_HARD_MUTATION).string()
  postprocess_string = compose(apply_mutation, DO_POSTPROCESSING).string()
  return postprocess_string


def NormalizeBretonSpirantMutation(breton_string: str) -> str:
  """Apply the Breton spirant mutation."""
  preprocess_string = compose(breton_string.strip().lower(), DO_PREPROCESSING).string()
  apply_mutation = compose(preprocess_string, DO_SPIRANT_MUTATION).string()
  postprocess_string = compose(apply_mutation, DO_POSTPROCESSING).string()
  return postprocess_string


def NormalizeBreton(breton_string: str) -> str:
  """Apply the Breton soft, hard, and spirant mutations. Ignores mixed mutation for now."""
  return NormalizeBretonSoftMutation(NormalizeBretonHardMutation(NormalizeBretonSpirantMutation(breton_string.strip().lower())))

