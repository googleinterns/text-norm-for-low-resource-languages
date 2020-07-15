!/usr/bin/env python
"""Library of language-agnostic FST rewrite rules to normalize text."""

import unicodedata
from dataclasses import dataclass
from typing import List
from pynini import *
import conf
from config import *


LANGUAGE = conf.LANGUAGE

GRAPHEMES = LANGUAGE.GRAPHEMES

INITIAL_PUNCTUATION = LANGUAGE.INITIAL_PUNCTUATION
FINAL_PUNCTUATION = LANGUAGE.FINAL_PUNCTUATION
OTHER_PUNCTUATION = union(r"\[", r"\]")
PUNCTUATION = union(INITIAL_PUNCTUATION, FINAL_PUNCTUATION, OTHER_PUNCTUATION)
NUMBERS = LANGUAGE.NUMBERS
SPACE = acceptor(" ")
UNDERSCORE = acceptor("_")

SIGMA_STAR = union(*("[{}]".format(i) for i in range(1, 256))
                   ).optimize().closure()


@dataclass
class Verbalizable:
    """Contains verbalizable tokens."""

    @staticmethod
    def verbalizable():
        """Returns union of verbalizable tokens.

        args: none

        returns: Union of acceptors for verbalizable tokens.
        """
        token = (INITIAL_PUNCTUATION.ques +
                 (GRAPHEMES.plus | NUMBERS.plus).plus +
                 FINAL_PUNCTUATION.ques)

        email_address = (union(GRAPHEMES, NUMBERS, UNDERSCORE, ".").plus +
                         "@" +
                         GRAPHEMES.plus +
                         closure("." + GRAPHEMES.plus, 1, 2))

        web_address = ((("http" + acceptor("s").ques + "://").ques +
                        "www.").ques +
                       union(GRAPHEMES, NUMBERS).plus +
                       closure("." + GRAPHEMES.plus, 1, 2) +
                       ("/" | ("/" + union(GRAPHEMES, NUMBERS)).star))

        # For times. Two numbers, a colon, followed by two more numbers,
        # optionally followed by another colon and two numbers.
        # Typically e.g. 12:25, but also 12:25:04 for seconds.
        # Will allow non-standard times like 40:70:80 !
        time = (closure(NUMBERS, 1, 2) +
                closure(":" + closure(NUMBERS, 1, 2), 1, 2))

        # For large numbers. Allows either 1-6 numerals, e.g. 150000;
        # 1-6 numerals followed by a decimal separator and up to 4 decimals,
        # e.g. 2552.4575; or allows 1-3 numerals followed by a grouping
        # separator, 1-3 more numerals, a decimal separator, and 1-4 more
        # numerals, e.g. 120,000.65
        # Will allow non-standard things like 50,00,00 !
        fancy_numbers = (closure(NUMBERS, 1, 6) |
                         (closure(NUMBERS, 1, 6)
                          + union(",", ".") + closure(NUMBERS, 1, 4)) |
                         ((closure(NUMBERS, 1, 3) +
                           union(",", ".")).ques +
                          closure(NUMBERS, 1, 3) +
                          (union(",", ".") +
                           closure(NUMBERS, 1, 4).ques)))

        return union(token, email_address, web_address, time, fancy_numbers)


# Remove all extra whitespace between words
# e.g. "hi      there" -> "hi there"

REMOVE_EXTRA_WHITESPACE = cdrewrite(
    transducer(SPACE, ""),
    "",
    SPACE,
    SIGMA_STAR)


# Language-specific formatting fixes

LANGUAGE_SPECIFIC_NORM = LANGUAGE.LANGUAGE_SPECIFIC_PREPROCESSING


#Discard invalid tokens
# e.g. "how are you today товарищ?" -> "how are you today?"


def pass_only_valid_tokens(string: str) -> str:
    """Replaces invalid strings in a sentence.

    Args:
        string: A line from a corpus.

    Returns:
        The line, where invalid tokens have been replaced with <UNK>.
    """
    valid_token = INITIAL_PUNCTUATION.ques + Verbalizable.verbalizable() + FINAL_PUNCTUATION.ques
    returned: List[str] = []
    remove_extra_whitespace = (string @ REMOVE_EXTRA_WHITESPACE).string()
    split_string = remove_extra_whitespace.split(" ")
    for token in split_string:
        if difference(acceptor(token), valid_token).num_states() == 0:
            returned.append(token)
        else:
            returned.append("<UNK>")
    return " ".join(returned)


def pass_only_valid_sentences(string: str) -> str:
    """Replaces invalid sentences.

    Args:
        string: A line from a corpus.

    Returns:
        The line or the line replaced with <SENTENCE_REJECTED>.
    """
    valid_token = INITIAL_PUNCTUATION.ques + Verbalizable.verbalizable() + FINAL_PUNCTUATION.ques
    remove_extra_whitespace = (string @ REMOVE_EXTRA_WHITESPACE).string()
    split_string = remove_extra_whitespace.split(" ")
    for token in split_string:
        if difference(acceptor(token), valid_token).num_states() != 0:
            return "<SENTENCE_REJECTED>"
    return string


# Detach punctuation from words
# e.g. "Who are you?" -> "Who are you ?"

NON_GRAPHEME_PUNCT = difference(PUNTUATION, GRAPHEMES)

INSERT_SPACE = transducer("", SPACE)

SEPARATE_PUNCTUATION = (
    cdrewrite(
        INSERT_SPACE,
        union("[BOS]", SPACE) + union(NON_GRAPHEME_PUNCT),
        (union(PUNCTUATION, Verbalizable.verbalizable()) +
         union("[EOS]", SPACE, Verbalizable.verbalizable())),
        SIGMA_STAR) @
    cdrewrite(
        INSERT_SPACE,
        union(Verbalizable.verbalizable(), PUNCTUATION),
        PUNCTUATION + union("[EOS]", SPACE, PUNCTUATION),
        SIGMA_STAR))


# Delete freestanding punctuation
# e.g. "hi there ?" -> "hi there

DELETE_PUNCTUATION = transducer(PUNCTUATION, "")

DELETE_FREESTANDING_PUNCTUATION = cdrewrite(
    DELETE_PUNCTUATION,
    union("[BOS]", SPACE),
    union("[EOS]", SPACE),
    SIGMA_STAR)


def apply_fst_rules(string: str) -> str:
    """Applies FST rewrite rules."""
    return string if (string == "<STRING_REJECTED>") else (
        string
        @ LANGUAGE_SPECIFIC_NORM
        @ SEPARATE_PUNCTUATION
        @ DELETE_FREESTANDING_PUNCTUATION
        @ REMOVE_EXTRA_WHITESPACE
        ).optimize().string()


def token_normalizer(string: str) -> str:
    """Normalizes text by applying FST rewrite rules.

    Args:
        string: A line from a corpus.

    Returns:
        The normalized line from the corpus.
    """
    string = unicodedata.normalize("NFC", string.lower())
    filtered_string = pass_only_valid_tokens(string)
    return apply_fst_rules(filtered_string)


def sentence_normalizer(string: str) -> str:
    """Normalizes text by applying FST rewrite rules.

    Args:
        string: A line from a corpus.

    Returns:
        The normalized line from the corpus.
    """
    string = unicodedata.normalize("NFC", string.lower())
    filtered_string = pass_only_valid_sentences(string)
    return apply_fst_rules(filtered_string)
