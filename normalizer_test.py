# Lint as: python3
"""Tests for evaluating text normalizer."""

import unittest
import normalizer_lib

class TestNormalizer(unittest.TestCase):
    """Tests for evaluating text normalizer."""


    def test_normalizer(self):
        'Test the output of normalizer.'
        with open("testdata/normalized_sentences.tsv", "r") as test_file:
            test_cases = test_file.readlines()[1:]
        for sentence in test_cases:
            with self.subTest(sentence=sentence):
                test_case = sentence.strip().split("\t")[1]
                expected = sentence.strip().split("\t")[2]
                test_fst = normalizer_lib.normalizer(test_case)
                self.assertEqual(test_fst, expected)


    def test_remove_extra_whitespace(self):
        'Test removing extra whitespace.'
        for test in [(("hi       there", "hi there"),
                      ("my friend    ", "my friend "),
                      ("   the sun", " the sun"),
                      ("   all   the   spaces   ", " all the spaces "))]:
            for test_case, expected in test:
                with self.subTest(test_case=test_case):
                    normalized_text = (test_case @
                                       normalizer_lib.DO_REMOVE_EXTRA_WHITESPACE
                                       ).string()
                    self.assertEqual(normalized_text, expected)


    def test_separate_punctuation(self):
        'Test separating punctuation from tokens.'
        for test in [(("hello, friend",
                       "hello , friend"),
                      ("the end.",
                       "the end ."),
                      ('"What',
                       '" What'),
                      ('"Who, he asked, left?"',
                       '" Who , he asked , left ? "'),
                      ("Don't separate apostrophes",
                       "Don't separate apostrophes"),
                      ("Keep ice-cream together",
                       "Keep ice-cream together"))]:
            for test_case, expected in test:
                with self.subTest(test_case=test_case):
                    normalized_text = (test_case @
                                       normalizer_lib.DO_SEPARATE_PUNCTUATION
                                       ).string()
                    self.assertEqual(normalized_text, expected)


    def test_delete_freestanding_punctuation(self):
        'Test deleting freestanding punctuation.'
        for test in [(("hello , friend", "hello  friend"),
                      ("the end .", "the end "),
                      ('" What', ' What'),
                      ('" Who , he asked , left ? "', ' Who  he asked  left  '))]:
            for test_case, expected in test:
                with self.subTest(test_case=test_case):
                    normalized_text = (test_case @
                                       normalizer_lib.DO_DELETE_FREESTANDING_PUNCTUATION
                                       ).string()
                    self.assertEqual(normalized_text, expected)


    def test_pass_only_valid(self):
        'Test deleting tokens not in language.'
        for test in [(("hello, товарищ", "hello, <REJECTED_TOKEN>"),
                      ("ABCÄÖÜß", "<REJECTED_TOKEN>"),
                      ("Где мой dog?", "<REJECTED_TOKEN> <REJECTED_TOKEN> dog?"))]:
            for test_case, expected in test:
                with self.subTest(test_case=test_case):
                    normalized_text = normalizer_lib.pass_only_valid(test_case)
                    self.assertEqual(normalized_text, expected)

if __name__ == '__main__':
    unittest.main()
