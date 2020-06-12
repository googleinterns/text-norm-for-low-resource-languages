import unittest
import normalize_breton_lib

class TestStringMethods(unittest.TestCase):

    def test_normalize_breton(self):
        'Test the output of NormalizeBreton.'
        test_cases = [(('a--bd', 'a-bd'), ('ddb--a', 'ddb-a'), ('ba--aa', 'ba-aa'))]
        for test in test_cases:
          for test_case, expected in test:
            test_fst = normalize_breton_lib.NormalizeBreton(test_case)
            self.assertEqual(test_fst, expected)


    def test_normalize_breton_soft_mutation(self):
        'Test the output of NormalizeBretonSoftMutation.'
        test_cases = [(("div plac'h", "div blac'h"), ("da tra", "da dra"), ("da kemper", "da gemper"), ("da gwin", "da win"), ("pe mamm", "pe vamm"))]
        # see what's going on with capital letters, Kemper and Gemper should be
        # capitalized
        for test in test_cases:
          for test_case, expected in test:
            test_fst = normalize_breton_lib.NormalizeBretonSoftMutation(test_case)
            self.assertEqual(test_fst, expected)

    def test_normalize_breton_hard_mutation(self):
        'Test the output of NormalizeBretonHardMutation.'
        test_cases = [(("da'z bag", "da'z pag"), ('ez douarn', 'ez touarn'), ('ho geriadur', 'ho keriadur'), ("ho gwenn-ha-du", "ho kwenn-ha-du"))]
        # Gwenn, Du, and Kwenn should be capitalized
        for test in test_cases:
          for test_case, expected in test:
            test_fst = normalize_breton_lib.NormalizeBretonHardMutation(test_case)
            self.assertEqual(test_fst, expected)

    def test_normalize_breton_spirant_mutation(self):
        'Test the output of NormalizeBretonSpirantMutation.'
        test_cases = [(('tri pesk', 'tri fesk'), ('hon tad', 'hon zad'), ('nav ki', "nav c'hi"))]
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
