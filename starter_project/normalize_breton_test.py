"""Tests for evaluating Celtic initial consonant mutations."""

import unittest
import normalize_breton_lib

class TestStringMethods(unittest.TestCase):
    """Tests for evaluating initial consonant mutations."""


    def test_normalize_breton(self):
        'Test the output of normalize_breton.'
        with open("testdata/bre_normalized_sentences.tsv", "r") as test_file:
            test_cases = test_file.readlines()[1:]
        for sentence in test_cases:
            with self.subTest(sentence=sentence):
                test_case = sentence.strip().split("\t")[1]
                expected = sentence.strip().split("\t")[2]
                test_fst = normalize_breton_lib.normalize_breton(test_case)
                self.assertEqual(test_fst, expected)


    def test_normalize_breton_soft_mutation(self):
        'Test the Breton soft mutation.'
        for test in [(("Div plac'h", "div blac'h"),
                      ("DA TRA", "da dra"),
                      ("da Kemper", "da gemper"),
                      ("da gwin", "da win"),
                      ("pe mamm", "pe vamm"))]:
            for test_case, expected in test:
                with self.subTest(test_case=test_case):
                    normalized_text = (
                        normalize_breton_lib.apply_single_mutation(
                            test_case, "soft"))
                    self.assertEqual(normalized_text, expected)


    def test_normalize_breton_soft_mutation_no_mutation(self):
        'Test the Breton soft mutation on words that should not mutate'
        for test in [(("bara kozh", "bara kozh"),
                      ("Bara ha kig", "bara ha kig"))]:
            for test_case, expected in test:
                with self.subTest(test_case=test_case):
                    normalized_text = (
                        normalize_breton_lib.apply_single_mutation(
                            test_case, "soft"))
                    self.assertEqual(normalized_text, expected)


    def test_normalize_breton_hard_mutation(self):
        'Test the Breton hard mutation.'
        for test in [(("da'z bag", "da'z pag"),
                      ('ho geriadur', 'ho keriadur'),
                      ("ho Gwenn-ha-Du", "ho kwenn-ha-du"))]:
            for test_case, expected in test:
                with self.subTest(test_case=test_case):
                    normalized_text = (
                        normalize_breton_lib.apply_single_mutation(
                            test_case, "hard"))
                    self.assertEqual(normalized_text, expected)


    def test_normalize_breton_spirant_mutation(self):
        'Test the Breton spirant mutation'
        for test in [(('tri pesk', 'tri fesk'),
                      ('Hon tad', 'hon zad'),
                      ('nav ki', "nav c'hi"))]:
            for test_case, expected in test:
                with self.subTest(test_case=test_case):
                    normalized_text = (
                        normalize_breton_lib.apply_single_mutation(
                            test_case, "spirant"))
                    self.assertEqual(normalized_text, expected)


if __name__ == '__main__':
    unittest.main()
