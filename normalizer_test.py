# Lint as: python3
"""Tests for evaluating text normalizer."""

import unittest
import normalizer_lib

class TestStringMethods(unittest.TestCase):
    """Tests for evaluating text normalizer."""


    def test_normalize_everything(self):
        'Test the output of normalize_everything.'
        with open("testdata/normalized_sentences.tsv", "r") as test_file:
            test_cases = test_file.readlines()[1:]
        for sentence in test_cases:
            with self.subTest(sentence=sentence):
                test_case = sentence.strip().split("\t")[1]
                expected = sentence.strip().split("\t")[2]
                test_fst = normalizer_lib.normalize_everything(test_case)
                self.assertEqual(test_fst, expected)


if __name__ == '__main__':
      unittest.main()
