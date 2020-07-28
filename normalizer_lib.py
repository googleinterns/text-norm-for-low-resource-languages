#/usr/bin/env python
"""Library of language-agnostic FST rewrite rules to normalize text."""

import importlib
import unicodedata
from typing import List
from pynini import *
from pynini.lib import byte, pynutil

class NormalizerLib:
    """Loads language-specific information for the text normalizer."""

    def __init__(self, language):
        self.language = importlib.import_module("config."+language)
        self.graphemes = self.language.GRAPHEMES
        self.initial_punctuation = self.language.INITIAL_PUNCTUATION
        self.final_punctuation = self.language.FINAL_PUNCTUATION
        self.other_punctuation = union(r"\[", r"\]")
        self.punctuation = union(self.initial_punctuation,
                                 self.final_punctuation,
                                 self.other_punctuation)
        self.non_grapheme_punctuation = difference(self.punctuation,
                                                   self.graphemes)
        self.numerals = self.language.NUMERALS
        self.sigma_star = byte.BYTES.closure()

        self.dummy_rewrite = cdrewrite(cross("", ""), "", "", self.sigma_star)
        try:
            self.language_specific_preprocessing = (
                self.language.LANGUAGE_SPECIFIC_PREPROCESSING)
        except Exception:
            self.language_specific_preprocessing = self.dummy_rewrite
        self.remove_extra_whitespace = cdrewrite(
            pynutil.delete(byte.SPACE),
            "",
            union(byte.SPACE, "[EOS]"),
            self.sigma_star)
        self.detach_leading_punctuation = cdrewrite(
            pynutil.insert(" "),
            union("[BOS]", byte.SPACE) + self.non_grapheme_punctuation.plus,
            union(self.non_grapheme_punctuation,
                  self.graphemes,
                  self.numerals),
            self.sigma_star)
        self.detach_trailing_punctuation = cdrewrite(
            pynutil.insert(" "),
            union(self.non_grapheme_punctuation,
                  self.graphemes,
                  self.numerals,
                  "/"),
            self.punctuation.plus + union("[EOS]", byte.SPACE),
            self.sigma_star)
        self.delete_freestanding_punctuation = cdrewrite(
            pynutil.delete(self.punctuation),
            union("[BOS]", byte.SPACE),
            union("[EOS]", byte.SPACE),
            self.sigma_star)


    def verbalizable(self):
        """Returns union of verbalizable tokens.

        Args: None

        Returns: Union of acceptors for verbalizable tokens.
        """
        token = (self.initial_punctuation.ques +
                 (self.graphemes | self.numerals).plus +
                 self.final_punctuation.ques).optimize()

        email_address = (self.initial_punctuation.ques +
                         union(self.graphemes, self.numerals, "_", ".").plus +
                         "@" +
                         self.graphemes.plus +
                         closure("." + self.graphemes.plus, 1, 2) +
                         self.final_punctuation.star).optimize()

        web_address = (self.initial_punctuation.ques +
                       (("http" + acceptor("s").ques + "://").ques +
                        "www.").ques +
                       union(self.graphemes, self.numerals).plus +
                       closure("." + self.graphemes.plus, 1, 2) +
                       ("/" + union(self.graphemes, self.numerals).star).star +
                       self.final_punctuation.star).optimize()

        # For times. Two numbers, a colon, followed by two more numbers,
        # optionally followed by another colon and two numbers.
        # Typically e.g. 12:25, but also 12:25:04 for seconds.
        # Will allow non-standard times like 40:70:80 !
        times = (closure(self.numerals, 1, 2) +
                 closure(":" + closure(self.numerals, 1, 2), 1, 2)).optimize()

        # For large numbers. Allows either 1-6 numerals, e.g. 150000;
        # 1-6 numerals followed by a decimal separator and up to 4 decimals,
        # e.g. 2552.4575; or allows 1-3 numerals followed by a grouping
        # separator, 1-3 more numerals, a decimal separator, and 1-4 more
        # numerals, e.g. 120,000.65
        # Will allow non-standard things like 50,00,00 !
        fancy_numbers = (closure(self.numerals, 1, 6) |
                         (closure(self.numerals, 1, 6)
                          + union(",", ".") + closure(self.numerals, 1, 4)) |
                         ((closure(self.numerals, 1, 3) +
                           union(",", ".")).ques +
                          closure(self.numerals, 1, 3) +
                          (union(",", ".") +
                           closure(self.numerals, 1, 4).ques))).optimize()
        return union(token, email_address, web_address, times, fancy_numbers).optimize()


    def split_into_tokens(self, string) -> List[str]:
        """Splits a string into a list of strings.

        Args:
            string: A line from a corpus.

        Returns:
            The line, split into a list of tokens.
        """
        return (string @ self.remove_extra_whitespace
                ).optimize().string().split(" ")


    def pass_only_valid_tokens(self, string) -> List[str]:
        """Replaces invalid strings in a sentence.

        Args:
            string: A line from a corpus.

        Returns:
            The line, where invalid tokens have been replaced with <UNK>.
        """
        returned: List[str] = []
        for token in self.split_into_tokens(string):
            if difference(acceptor(token), self.verbalizable()
                          ).num_states() == 0:
                returned.append(token)
            else:
                returned.append("<UNK>")
        return " ".join(returned)


    def pass_only_valid_sentences(self, string) -> List[str]:
        """Replaces invalid sentences.

        Args:
            string: A line from a corpus.

        Returns:
            The line or the line replaced with <SENTENCE_REJECTED>.
        """
        for token in self.split_into_tokens(string):
            if difference(acceptor(token), self.verbalizable()).num_states() != 0:
                return "<SENTENCE_REJECTED>"
        return string


    def apply_fst_rules(self, string: str) -> str:
        """Applies FST rewrite rules."""
        return string if (string == "<STRING_REJECTED>") else (
            string
            @ self.language_specific_preprocessing
            @ self.detach_leading_punctuation
            @ self.detach_trailing_punctuation
            @ self.delete_freestanding_punctuation
            @ self.remove_extra_whitespace
            ).optimize().string()


    def preprocess_string(self, string: str, normalizer: str) -> str:
        """Prepares a string to pass through the normalizer.

        Takes a line of the corpus as input, lowercases it and performs
        NFC unicode normalization, and filters it using the token-
        or sentence-based filter.

        Note that string.lower() may not work for all scripts!

        Args:
            string:  The string to preprocess.

        Returns:
            The preprocessed string to pass to the FST rules.
        """
        lowercase_string = string.lower()
        unicode_normalize = unicodedata.normalize("NFC", lowercase_string)
        if normalizer == "sentence":
            filter_string = self.pass_only_valid_sentences(
                unicode_normalize)
        else:
            filter_string = self.pass_only_valid_tokens(
                unicode_normalize)
        return filter_string


    def token_normalizer(self, string: str) -> str:
        """Normalizes text by applying FST rewrite rules.

        Args:
            string: A line from a corpus.

        Returns:
            The normalized line from the corpus.
        """
        return self.apply_fst_rules(self.preprocess_string(string, "token"))


    def sentence_normalizer(self, string: str) -> str:
        """Normalizes text by applying FST rewrite rules.

        Args:
            string: A line from a corpus.

        Returns:
            The normalized line from the corpus.
        """
        return self.apply_fst_rules(self.preprocess_string(string, "sentence"))
