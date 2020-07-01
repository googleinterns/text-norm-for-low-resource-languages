#!/usr/bin/env python
"""Library of language-agnostic FST rewrite rules to normalize text."""

import unicodedata
from pynini import *
from config import *

LANGUAGE = af

GRAPHEMES = LANGUAGE.GRAPHEMES

INITIAL_PUNCTUATION = LANGUAGE.INITIAL_PUNCTUATION
FINAL_PUNCTUATION = LANGUAGE.FINAL_PUNCTUATION
OTHER_PUNCTUATION = union(r"\[", r"\]")
PUNCTUATION = union(INITIAL_PUNCTUATION, FINAL_PUNCTUATION, OTHER_PUNCTUATION)
NUMBERS = union("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
SPACE = acceptor(" ")

VALID_WORDS = union(
    GRAPHEMES.plus,
    PUNCTUATION.plus,
    NUMBERS.plus,
    SPACE.plus).optimize()

SIGMA_STAR = union(*("[{}]".format(i) for i in range(1, 256))
                   ).optimize().closure()


# Step 1: Remove all extra whitespace between words

REMOVE_EXTRA_WHITESPACE = transducer(SPACE.plus, SPACE)

DO_REMOVE_EXTRA_WHITESPACE = cdrewrite(
    REMOVE_EXTRA_WHITESPACE,
    union(GRAPHEMES, PUNCTUATION),
    union(GRAPHEMES, PUNCTUATION),
    SIGMA_STAR)


# Step 2: Language-specific formatting fixes

DO_LANGUAGE_SPECIFIC_PREPROCESSING = LANGUAGE.LANGUAGE_SPECIFIC_PREPROCESSING


# Step 3: Apply NFC unicode normalize
# really slow when done this way,
# super fast when I just call unicodedata.normalize
# on the string at the beginning
# may remove later
#def unicode_normalize(string: str) -> Fst:
#    "Normalizes unicode to NFC normalization."
#    nfc_normalized = unicodedata.normalize("NFC", string)
#    normalizer = transducer(string, nfc_normalized).optimize()
#    return cdrewrite(normalizer, "", "", SIGMA_STAR).optimize()


# Step 4: Discard examples not associated with a pronunciation
# e.g. "how are you today товарищ?" -> "how are you today?"
# FIXME: not working yet


#def pass_only_valid(string: str) -> Fst:
#    "Accept only valid sentences in the language."
#    STRING = acceptor(string).optimize()
#    OVERLAP = intersect(STRING, VALID_WORDS.plus).optimize()
#    VALID_STRING = "***REJECT***"
#    VALID_STRING = STRING if (OVERLAP == STRING) else acceptor("***REJECT***")
#    TRANSDUCE_VALID_STRING = transducer(STRING, VALID_STRING)
#    return cdrewrite(TRANSDUCE_VALID_STRING, "", "", SIGMA_STAR)


NONWORDS = union("т", "о", "в")

DISCARD_NONWORDS = transducer(NONWORDS.plus, "")

DO_DISCARD_NONWORDS = cdrewrite(
    DISCARD_NONWORDS,
    "",
    "",
    SIGMA_STAR)


# Step 5: Detach punctuation from words
# e.g. "Who are you?" -> "Who are you ?"

SEPARATE_PUNCTUATION = transducer("", SPACE)

DO_SEPARATE_PUNCTUATION = (
    cdrewrite(
        SEPARATE_PUNCTUATION,
        union(GRAPHEMES, PUNCTUATION),
        PUNCTUATION,
        SIGMA_STAR) @
    cdrewrite(
        SEPARATE_PUNCTUATION,
        PUNCTUATION,
        union(GRAPHEMES, PUNCTUATION),
        SIGMA_STAR))


# Step 7: Delete freestanding punctuation
# e.g. "hi there ?" -> "hi there

DELETE_FREESTANDING_PUNCTUATION = transducer(PUNCTUATION, "")

DO_DELETE_FREESTANDING_PUNCTUATION = cdrewrite(
    DELETE_FREESTANDING_PUNCTUATION,
    SPACE,
    "",
    SIGMA_STAR)


def normalize_everything(string: str) -> str:
    "Applies FST rewrite rules to normalize text."
    string = unicodedata.normalize("NFC", string.lower())
    return (string
            #@ DO_REMOVE_EXTRA_WHITESPACE
            @ DO_LANGUAGE_SPECIFIC_PREPROCESSING
            #@ unicode_normalize(string) ## SLOW, doing this above instead
            @ DO_SEPARATE_PUNCTUATION
            @ DO_DELETE_FREESTANDING_PUNCTUATION
            @ DO_REMOVE_EXTRA_WHITESPACE
            ).optimize().string()
