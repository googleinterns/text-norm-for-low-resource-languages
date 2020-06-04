#python 3
'''Add docstring.''' 

import pynini

BR_GRAPHEMES = pynini.union("a", "b", "c")
HYPHEN = "-"
sigma_star = pynini.union(BR_GRAPHEMES, HYPHEN).closure()

DELETE_HYPHEN = pynini.transducer(HYPHEN, "")

REMOVE_EXTRA_HYPHEN_IN_WORD = pynini.cdrewrite(
  DELETE_HYPHEN,
  BR_GRAPHEMES + pynini.acceptor(HYPHEN).ques,
  pynini.acceptor(HYPHEN).ques + BR_GRAPHEMES,
  sigma_star) 

def NormalizeBreton() -> pynini.Fst:
  return REMOVE_EXTRA_HYPHEN_IN_WORD
