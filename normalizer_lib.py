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
        self.numerals = self.language.NUMERALS
        try:
            self.language_specific_preprocessing = self.language.LANGUAGE_SPECIFIC_PREPROCESSING
        except Exception:
            self.language_specific_preprocessing = None

    SIGMA_STAR = byte.BYTES.closure()
    UNDERSCORE = acceptor("_")

    def verbalizable(self):

        """Returns union of verbalizable tokens.

        Args: None

        Returns: Union of acceptors for verbalizable tokens.
        """
        token = (self.initial_punctuation.ques +
                 (self.graphemes.plus | self.numerals.plus).plus +
                 self.final_punctuation.ques).optimize()

        email_address = (self.initial_punctuation.ques +
                         union(self.graphemes, self.numerals, self.UNDERSCORE, ".").plus +
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


    # Remove all extra whitespace between words
    # e.g. "hi      there" -> "hi there"


    def remove_extra_whitespace(self) -> Fst:
        "Removes extra whitespace."
        remove_extra_whitespace = cdrewrite(
            pynutil.delete(byte.SPACE),
            "",
            byte.SPACE,
            self.SIGMA_STAR)
        return remove_extra_whitespace


    # Language-specific formatting fixes


    def language_specific_fixes(self) -> Fst:
        "Applies language-specific formatting fixes."
        if self.language_specific_preprocessing:
            return self.language_specific_preprocessing
        generic_fst = cdrewrite(cross("", ""), "", "", self.SIGMA_STAR)
        return generic_fst


    #Discard invalid tokens
    # e.g. "how are you today товарищ?" -> "how are you today?"


    def pass_only_valid_tokens(self, string) -> List[str]:
        """Replaces invalid strings in a sentence.

        Args:
            string: A line from a corpus.

        Returns:
            The line, where invalid tokens have been replaced with <UNK>.
        """
        valid_token = (self.initial_punctuation.ques +
                       self.verbalizable() +
                       self.final_punctuation.ques)
        returned: List[str] = []
        remove_extra_whitespace = (string @ self.remove_extra_whitespace()).optimize().string()
        split_string = remove_extra_whitespace.split(" ")
        for token in split_string:
            if difference(acceptor(token), valid_token).num_states() == 0:
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
        valid_token = (self.initial_punctuation.ques +
                       self.verbalizable() +
                       self.final_punctuation.ques)
        remove_extra_whitespace = (string @ self.remove_extra_whitespace()).optimize().string()
        split_string = remove_extra_whitespace.split(" ")
        for token in split_string:
            if difference(acceptor(token), valid_token).num_states() != 0:
                return "<SENTENCE_REJECTED>"
        return string


    # Detach punctuation from words
    # e.g. "Who are you?" -> "Who are you ?"


    def detach_punctuation(self) -> Fst:
        "Detaches punctuation from words."
        non_grapheme_punct = difference(self.punctuation, self.graphemes)
        detach_leading_punctuation = cdrewrite(
            pynutil.insert(" "),
            union("[BOS]", byte.SPACE) + non_grapheme_punct.plus,
            union(non_grapheme_punct, self.graphemes, self.numerals),
            self.SIGMA_STAR)
        detach_trailing_punctuation = cdrewrite(
            pynutil.insert(" "),
            union(non_grapheme_punct, self.graphemes, self.numerals, "/"),
            self.punctuation.plus + union("[EOS]", byte.SPACE),
            self.SIGMA_STAR)
        return (detach_leading_punctuation @ detach_trailing_punctuation).optimize()


    # Delete freestanding punctuation
    # e.g. "hi there ?" -> "hi there


    def delete_freestanding_punctuation(self) -> Fst:
        "Deletes freestanding punctuation."
        delete_freestanding_punctuation = cdrewrite(
            pynutil.delete(self.punctuation),
            union("[BOS]", byte.SPACE),
            union("[EOS]", byte.SPACE),
            self.SIGMA_STAR)
        return delete_freestanding_punctuation


    def apply_fst_rules(self, string: str) -> str:
        """Applies FST rewrite rules."""
        return string if (string == "<STRING_REJECTED>") else (
            string
            @ self.language_specific_fixes()
            @ self.detach_punctuation()
            @ self.delete_freestanding_punctuation()
            @ self.remove_extra_whitespace()
            ).optimize().string()


    def token_normalizer(self, string: str) -> str:
        """Normalizes text by applying FST rewrite rules.

        Args:
            string: A line from a corpus.

        Returns:
            The normalized line from the corpus.
        """
        string = unicodedata.normalize("NFC", string.lower())
        filtered_string = self.pass_only_valid_tokens(string)
        return self.apply_fst_rules(filtered_string).strip()


    def sentence_normalizer(self, string: str) -> str:
        """Normalizes text by applying FST rewrite rules.

        Args:
            string: A line from a corpus.

        Returns:
            The normalized line from the corpus.
        """
        string = unicodedata.normalize("NFC", string.lower())
        filtered_string = self.pass_only_valid_sentences(string)
        return self.apply_fst_rules(filtered_string).strip()
