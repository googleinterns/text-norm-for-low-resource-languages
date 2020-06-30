#!/usr/bin/env python
"""Library of language-agnostic FST rewrite rules to normalize text."""

from pynini import *
import unicodedata
from config import *

language = af

GRAPHEMES = language.GRAPHEMES

INITIAL_PUNCTUATION = language.INITIAL_PUNCTUATION
FINAL_PUNCTUATION = language.FINAL_PUNCTUATION

PUNCTUATION = union(INITIAL_PUNCTUATION, FINAL_PUNCTUATION)

NUMBERS = union("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

SPACE = acceptor(" ")

VALID_WORDS = union(GRAPHEMES.plus, PUNCTUATION.plus, NUMBERS.plus, SPACE.plus)

SIGMA_STAR = union(*("[{}]".format(i) for i in range(1, 256))).optimize().closure()


# Step 1: Remove all extra whitespace between words
# e.g. "hi     there" -> "hi there"

REMOVE_EXTRA_WHITESPACE = transducer(SPACE.plus, SPACE)

DO_REMOVE_EXTRA_WHITESPACE = cdrewrite(
    REMOVE_EXTRA_WHITESPACE,
    union(GRAPHEMES, PUNCTUATION),
    union(GRAPHEMES, PUNCTUATION),
    SIGMA_STAR)


# Step 2: Language-specific formatting fixes

DO_LANGUAGE_SPECIFIC_PREPROCESSING = language.LANGUAGE_SPECIFIC_PREPROCESSING


# Step 3: Lowercase all characters in languages with case
# e.g. "isiZulu" -> "isizulu"


def unicode_normalize(string: str) -> Fst:
    "Normalizes unicode to NFC normalization."
    NORMALIZER = transducer(string, unicodedata.normalize("NFC", string))
    return cdrewrite(NORMALIZER, "", "", SIGMA_STAR)


# Step 4: Discard examples not associated with a pronunciation
# e.g. "how are you today товарищ?" -> "how are you today?"

VALID_WORDS = GRAPHEMES.plus
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

DO_SEPARATE_PUNCTUATION = (cdrewrite(
                                    SEPARATE_PUNCTUATION,
                                    GRAPHEMES,
                                    PUNCTUATION,
                                    SIGMA_STAR) @
                           cdrewrite(
                                    SEPARATE_PUNCTUATION,
                                    PUNCTUATION,
                                    GRAPHEMES,
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
    "Apply language-agnostic rewrite rules."
    string = string.lower()
    return (string
#            @ DO_REMOVE_EXTRA_WHITESPACE
            @ DO_LANGUAGE_SPECIFIC_PREPROCESSING
            @ unicode_normalize(string)
            @ DO_DISCARD_NONWORDS
#            @ VALID_WORDS
            @ DO_SEPARATE_PUNCTUATION
            @ DO_DELETE_FREESTANDING_PUNCTUATION
            @ DO_REMOVE_EXTRA_WHITESPACE
            ).string()
