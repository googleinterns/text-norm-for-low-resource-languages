import unittest
import normalize_breton_lib as norm
import sys

class TestStringMethods(unittest.TestCase):


    def test_normalize_breton(self):
        'Test the output of NormalizeBreton.'
        with open("bre_normalized_sentences.tsv", "r") as filename:
          test_cases = filename.readlines()[1:]
#        test_cases = [(("ma gwin Da gwin tri pesk bara kozh ha KIG", "ma gwin da win tri fesk bara kozh ha kig"), ("da Kemper", "da gemper"))]
        for sentence in test_cases:
          test_case = sentence.strip().split("\t")[1]
          expected = sentence.strip().split("\t")[2]
          test_fst = norm.NormalizeBreton(test_case)
          self.assertEqual(test_fst, expected)


    def test_normalize_breton_soft_mutation(self):
        'Test the Breton soft mutation.'
        test_cases = [(("Div plac'h", "div blac'h"), ("DA TRA", "da dra"), ("da Kemper", "da gemper"), ("da gwin", "da win"), ("pe mamm", "pe vamm"))]
        for test in test_cases:
          for test_case, expected in test:
            preprocessed = norm.preprocess(test_case)
            test_fst = norm.apply_mutation(preprocessed, "soft")
            postprocessed = norm.postprocess(test_fst)
            self.assertEqual(postprocessed, expected)


    def test_normalize_breton_soft_mutation_no_mutation(self):
        'Test the Breton soft mutation on words that should not mutate'
        test_cases = [(("bara kozh", "bara kozh"), ("Bara ha kig", "bara ha kig"))]
        for test in test_cases:
          for test_case, expected in test:
            preprocessed = norm.preprocess(test_case)
            test_fst = norm.apply_mutation(preprocessed, "soft")
            postprocessed = norm.postprocess(test_fst)
            self.assertEqual(postprocessed, expected)


    def test_normalize_breton_hard_mutation(self):
        'Test the Breton hard mutation.'
        test_cases = [(("da'z bag", "da'z pag"), ('ez douarn', 'ez touarn'), ('ho geriadur', 'ho keriadur'), ("ho Gwenn-ha-Du", "ho kwenn-ha-du"))]
        for test in test_cases:
          for test_case, expected in test:
            preprocessed = norm.preprocess(test_case)
            test_fst = norm.apply_mutation(preprocessed, "hard")
            postprocessed = norm.postprocess(test_fst)
            self.assertEqual(postprocessed, expected)


    def test_normalize_breton_spirant_mutation(self):
        'Test the Breton spirant mutation'
        test_cases = [(('tri pesk', 'tri fesk'), ('Hon tad', 'hon zad'), ('nav ki', "nav c'hi"))]
        for test in test_cases:
          for test_case, expected in test:
            preprocessed = norm.preprocess(test_case)
            test_fst = norm.apply_mutation(preprocessed, "spirant")
            postprocessed = norm.postprocess(test_fst)
            self.assertEqual(postprocessed, expected)


if __name__ == '__main__':
    unittest.main()
