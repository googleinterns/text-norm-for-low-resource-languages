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
NUMBERS = LANGUAGE.NUMBERS
SPACE = acceptor(" ")

SIGMA_STAR = union(*("[{}]".format(i) for i in range(1, 256))
                   ).optimize().closure()


# Step 1: Remove all extra whitespace between words

REMOVE_EXTRA_WHITESPACE = cdrewrite(
    transducer(SPACE, ""),
    "",
    SPACE,
    SIGMA_STAR)


# Step 2: Language-specific formatting fixes

LANGUAGE_SPECIFIC_NORM = LANGUAGE.LANGUAGE_SPECIFIC_PREPROCESSING


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

SENTENCE = (INITIAL_PUNCTUATION.ques + (GRAPHEMES.plus | NUMBERS.plus) + FINAL_PUNCTUATION.ques +
            (SPACE.plus + GRAPHEMES.plus).star + FINAL_PUNCTUATION.ques)


def pass_only_valid_tokens(string: str) -> str:
    """Replaces invalid tokens in a sentence with <UNK>, keeps the rest.

    Args:
        string: A line from a corpus.

    Returns:
        The line, but where invalid tokens have been replaced by <UNK>.
    """
    valid_token = GRAPHEMES.plus
    returned: List[str] = []
    remove_extra_whitespace = (string @ REMOVE_EXTRA_WHITESPACE).string()
    split_string = remove_extra_whitespace.split(" ")
    for token in split_string:
        if difference(acceptor(token), SENTENCE).num_states() == 0:
            returned.append(token)
        else:
            returned.append("<UNK>")
    return " ".join(returned)


# Step 5: Detach punctuation from words
# e.g. "Who are you?" -> "Who are you ?"

INSERT_SPACE = transducer("", SPACE)

SEPARATE_PUNCTUATION = (
    cdrewrite(
        INSERT_SPACE,
        union(GRAPHEMES, PUNCTUATION),
        PUNCTUATION + union(PUNCTUATION, SPACE, "[EOS]"),
        SIGMA_STAR) @
    cdrewrite(
        INSERT_SPACE,
        union(PUNCTUATION, SPACE, "[BOS]") + PUNCTUATION,
        union(GRAPHEMES, PUNCTUATION),
        SIGMA_STAR))


# Step 7: Delete freestanding punctuation
# e.g. "hi there ?" -> "hi there

DELETE_PUNCTUATION = transducer(PUNCTUATION, "")

DELETE_FREESTANDING_PUNCTUATION = cdrewrite(
    DELETE_PUNCTUATION,
    union("[BOS]", SPACE),
    union("[EOS]", ""),
    SIGMA_STAR)


def normalizer(string: str) -> str:
    """Applies FST rewrite rules to normalize text.

    Args:
        string: A line from a corpus.

    Returns:
        The normalized line from the corpus.
    """
    string = unicodedata.normalize("NFC", string.lower())
    #filtered_string = string @ SENTENCE # for all-or-nothing filtering
    filtered_string = pass_only_valid_tokens(string) # for token-based filtering
    try:
        return (filtered_string
                #@ REMOVE_EXTRA_WHITESPACE
                @ LANGUAGE_SPECIFIC_NORM
                #@ unicode_normalize(string) ## SLOW, doing this above instead
                @ SEPARATE_PUNCTUATION
                @ DELETE_FREESTANDING_PUNCTUATION
                @ REMOVE_EXTRA_WHITESPACE
                ).optimize().string()
    except Warning:
        return "<STRING REJECTED>"
