import unittest
import normalize_breton_lib
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
          test_fst = normalize_breton_lib.NormalizeBreton(test_case)
          self.assertEqual(test_fst, expected)
#          for test_case, expected in test:
#            test_fst = normalize_breton_lib.NormalizeBreton(test_case)
#            self.assertEqual(test_fst, expected)


    def test_normalize_breton_soft_mutation(self):
        'Test the output of NormalizeBretonSoftMutation.'
        test_cases = [(("Div plac'h", "div blac'h"), ("DA TRA", "da dra"), ("da Kemper", "da gemper"), ("da gwin", "da win"), ("pe mamm", "pe vamm"))]
        for test in test_cases:
          for test_case, expected in test:
            test_fst = normalize_breton_lib.NormalizeBretonSoftMutation(test_case)
            self.assertEqual(test_fst, expected)


    def test_normalize_breton_soft_mutation_no_mutation(self):
        'Test the output of NormalizeBretonSoftMutation on words that should not mutate'
        test_cases = [(("bara kozh", "bara kozh"), ("Bara ha kig", "bara ha kig"))]
        for test in test_cases:
          for test_case, expected in test:
            test_fst = normalize_breton_lib.NormalizeBretonSoftMutation(test_case)
            self.assertEqual(test_fst, expected)


    def test_normalize_breton_hard_mutation(self):
        'Test the output of NormalizeBretonHardMutation.'
        test_cases = [(("da'z bag", "da'z pag"), ('ez douarn', 'ez touarn'), ('ho geriadur', 'ho keriadur'), ("ho Gwenn-ha-Du", "ho kwenn-ha-du"))]
        for test in test_cases:
          for test_case, expected in test:
            test_fst = normalize_breton_lib.NormalizeBretonHardMutation(test_case)
            self.assertEqual(test_fst, expected)


    def test_normalize_breton_spirant_mutation(self):
        'Test the output of NormalizeBretonSpirantMutation.'
        test_cases = [(('tri pesk', 'tri fesk'), ('Hon tad', 'hon zad'), ('nav ki', "nav c'hi"))]
        for test in test_cases:
          for test_case, expected in test:
            test_fst = normalize_breton_lib.NormalizeBretonSpirantMutation(test_case)
            self.assertEqual(test_fst, expected)

#    AZ: think about how to do mixed mutation, since all the triggers ("o", "e",
#    and "ma" are homographs with other triggers for different mutations
#    def test_normalize_breton_mixed_mutation(self):
#        'Test the output of NormalizeBretonMixedMutation.'
#        test_cases = [(("div plac'h", "div blac'h"), ('da t', 'da d'), ('da Kemper', 'da Gemper'), ("da gwin", "da win"), ('pe mamm', 'pe vamm'))]
#        for test in test_cases:
#          for test_case, expected in test:
#            test_fst = normalize_breton_lib.NormalizeBreton(test_case)
#            self.assertEqual(test_fst, expected)

if __name__ == '__main__':
    unittest.main()
