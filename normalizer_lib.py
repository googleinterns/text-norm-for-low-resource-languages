#/usr/bin/env python
"""Library of language-agnostic FST rewrite rules to normalize text."""

import importlib
import unicodedata
from typing import List
from pynini import *
import config.utils as utils

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

    SIGMA_STAR = utils.SIGMA_STAR
    SPACE = acceptor(" ")
    UNDERSCORE = acceptor("_")

    def verbalizable(self):
        """Returns union of verbalizable tokens.

        args: none

        returns: Union of acceptors for verbalizable tokens.
        """
        token = (self.initial_punctuation.ques +
                 (self.graphemes.plus | self.numerals.plus).plus +
                 self.final_punctuation.ques)

        email_address = (union(self.graphemes, self.numerals, self.UNDERSCORE, ".").plus +
                         "@" +
                         self.graphemes.plus +
                         closure("." + self.graphemes.plus, 1, 2))

        web_address = ((("http" + acceptor("s").ques + "://").ques +
                        "www.").ques +
                       union(self.graphemes, self.numerals).plus +
                       closure("." + self.graphemes.plus, 1, 2) +
                       ("/" | ("/" + union(self.graphemes, self.numerals)).star))

        # For times. Two numbers, a colon, followed by two more numbers,
        # optionally followed by another colon and two numbers.
        # Typically e.g. 12:25, but also 12:25:04 for seconds.
        # Will allow non-standard times like 40:70:80 !
        time = (closure(self.numerals, 1, 2) +
                closure(":" + closure(self.numerals, 1, 2), 1, 2))

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
                           closure(self.numerals, 1, 4).ques)))

        return union(token, email_address, web_address, time, fancy_numbers)


    # Remove all extra whitespace between words
    # e.g. "hi      there" -> "hi there"


    def remove_extra_whitespace(self, string: Fst) -> Fst:
        "Removes extra whitespace."
        print("Removing extra whitespace...")
        remove_extra_whitespace = cdrewrite(
            transducer(self.SPACE, ""),
            "",
            self.SPACE,
            self.SIGMA_STAR)
        return (string @ remove_extra_whitespace).optimize()


    # Language-specific formatting fixes


    def language_specific_fixes(self, string: Fst) -> Fst:
        "Applies language-specific formatting fixes."
        print("Applying language-specific fixes...")
        if self.language_specific_preprocessing:
            return (string @ self.language_specific_preprocessing).optimize()
        return string


    #Discard invalid tokens
    # e.g. "how are you today товарищ?" -> "how are you today?"


    def pass_only_valid_tokens(self, string) -> str:
        """Replaces invalid strings in a sentence.

        Args:
            string: A line from a corpus.

        Returns:
            The line, where invalid tokens have been replaced with <UNK>.
        """
        print("Replacing invalid tokens...")
        valid_token = (self.initial_punctuation.ques +
                       self.verbalizable() +
                       self.final_punctuation.ques)
        returned: List[str] = []
        remove_extra_whitespace = self.remove_extra_whitespace(string).string()
        split_string = remove_extra_whitespace.split(" ")
        for token in split_string:
            if difference(acceptor(token), valid_token).num_states() == 0:
                returned.append(token)
            else:
                returned.append("<UNK>")
        return " ".join(returned)


    def pass_only_valid_sentences(self, string) -> str:
        """Replaces invalid sentences.

        Args:
            string: A line from a corpus.

        Returns:
            The line or the line replaced with <SENTENCE_REJECTED>.
        """
        print("Replacing invalid sentences...")
        valid_token = (self.initial_punctuation.ques +
                       self.verbalizable() +
                       self.final_punctuation.ques)
        remove_extra_whitespace = self.remove_extra_whitespace(string).string()
        split_string = remove_extra_whitespace.split(" ")
        for token in split_string:
            if difference(acceptor(token), valid_token).num_states() != 0:
                return "<SENTENCE_REJECTED>"
        return string


    # Detach punctuation from words
    # e.g. "Who are you?" -> "Who are you ?"


    def detach_punctuation(self, string: Fst) -> Fst:
        "Detaches punctuation from words."
        print("Detaching punctuation from words...")
        non_grapheme_punct = difference(self.punctuation, self.graphemes)

        insert_space = transducer("", self.SPACE)

        separate_punctuation = (
            cdrewrite(
                insert_space,
                union("[BOS]", self.SPACE) + union(non_grapheme_punct),
                (union(self.punctuation, self.verbalizable()) +
                 union("[EOS]", self.SPACE, self.verbalizable())),
                self.SIGMA_STAR) @
            cdrewrite(
                insert_space,
                union(self.verbalizable(), self.punctuation),
                self.punctuation + union("[EOS]", self.SPACE, self.punctuation),
                self.SIGMA_STAR))
        return string @ separate_punctuation


    # Delete freestanding punctuation
    # e.g. "hi there ?" -> "hi there


    def delete_freestanding_punctuation(self, string: Fst) -> Fst:
        "Deletes freestanding punctuation."
        print("Deleting freestanding punctuation...")
        delete_freestanding_punctuation = cdrewrite(
            transducer(self.punctuation, ""),
            union("[BOS]", self.SPACE),
            union("[EOS]", self.SPACE),
            self.SIGMA_STAR)
        return (string @ delete_freestanding_punctuation).optimize()


    def apply_fst_rules(self, string: str) -> str:
        """Applies FST rewrite rules."""
        print("Applying all FST rewrite rules...")
        return string if (string == "<STRING_REJECTED>") else (
            self.remove_extra_whitespace(
                self.delete_freestanding_punctuation(
                    self.detach_punctuation(
                        self.language_specific_fixes(string)
                    )
                )
            )
        ).optimize().string()
#            string
#            @ self.language_specific_fixes(string)
#            @ self.detach_punctuation(string)
#            @ self.delete_freestanding_punctuation(string)
#            @ self.remove_extra_whitespace(string)
#            ).optimize().string()


    def token_normalizer(self, string: str) -> str:
        """Normalizes text by applying FST rewrite rules.

        Args:
            string: A line from a corpus.

        Returns:
            The normalized line from the corpus.
        """
        print("\nRunning token-based normalizer...")
        string = unicodedata.normalize("NFC", string.lower())
        filtered_string = self.pass_only_valid_tokens(string)
        return self.apply_fst_rules(filtered_string)


    def sentence_normalizer(self, string: str) -> str:
        """Normalizes text by applying FST rewrite rules.

        Args:
            string: A line from a corpus.

        Returns:
            The normalized line from the corpus.
        """
        print("\nRunning sentence-based normalizer...")
        string = unicodedata.normalize("NFC", string.lower())
        filtered_string = self.pass_only_valid_sentences(string)
        return self.apply_fst_rules(filtered_string)
