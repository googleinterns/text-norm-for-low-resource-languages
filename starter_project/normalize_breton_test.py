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
            test_case = sentence.strip().split("\t")[1]
            expected = sentence.strip().split("\t")[2]
            test_fst = normalize_breton_lib.normalize_breton(test_case)
            self.assertEqual(test_fst, expected)


    def test_normalize_breton_soft_mutation(self):
        'Test the Breton soft mutation.'
        test_cases = [(("Div plac'h", "div blac'h"),
                       ("DA TRA", "da dra"),
                       ("da Kemper", "da gemper"),
                       ("da gwin", "da win"),
                       ("pe mamm", "pe vamm"))]
        for test in test_cases:
            for test_case, expected in test:
                normalized_text = (test_case.strip().lower() @
                                   normalize_breton_lib.DO_PREPROCESSING @
                                   normalize_breton_lib.DO_SOFT_MUTATION @
                                   normalize_breton_lib.DO_POSTPROCESSING
                                   ).string()
                self.assertEqual(normalized_text, expected)


    def test_normalize_breton_soft_mutation_no_mutation(self):
        'Test the Breton soft mutation on words that should not mutate'
        test_cases = [(("bara kozh", "bara kozh"),
                       ("Bara ha kig", "bara ha kig"))]
        for test in test_cases:
            for test_case, expected in test:
                normalized_text = (test_case.strip().lower() @
                                   normalize_breton_lib.DO_PREPROCESSING @
                                   normalize_breton_lib.DO_SOFT_MUTATION @
                                   normalize_breton_lib.DO_POSTPROCESSING
                                   ).string()
                self.assertEqual(normalized_text, expected)


    def test_normalize_breton_hard_mutation(self):
        'Test the Breton hard mutation.'
        test_cases = [(("da'z bag", "da'z pag"),
                       ('ho geriadur', 'ho keriadur'),
                       ("ho Gwenn-ha-Du", "ho kwenn-ha-du"))]
        for test in test_cases:
            for test_case, expected in test:
                normalized_text = (test_case.strip().lower() @
                                   normalize_breton_lib.DO_PREPROCESSING @
                                   normalize_breton_lib.DO_HARD_MUTATION @
                                   normalize_breton_lib.DO_POSTPROCESSING
                                   ).string()
                self.assertEqual(normalized_text, expected)


    def test_normalize_breton_spirant_mutation(self):
        'Test the Breton spirant mutation'
        test_cases = [(('tri pesk', 'tri fesk'),
                       ('Hon tad', 'hon zad'),
                       ('nav ki', "nav c'hi"))]
        for test in test_cases:
            for test_case, expected in test:
                normalized_text = (test_case.strip().lower() @
                                   normalize_breton_lib.DO_PREPROCESSING @
                                   normalize_breton_lib.DO_SPIRANT_MUTATION @
                                   normalize_breton_lib.DO_POSTPROCESSING
                                   ).string()
                self.assertEqual(normalized_text, expected)


if __name__ == '__main__':
    unittest.main()
