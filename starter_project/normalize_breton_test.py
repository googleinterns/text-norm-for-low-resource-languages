import unittest
import normalize_breton_lib

class TestStringMethods(unittest.TestCase):

    def test_normalize_breton(self):
        'Test the output of NormalizeBreton.'
        test_cases = [(('a--bc', 'a-bc'), ('ccb--a', 'ccb-a'), ('ba--aa', 'ba-aa'))]
        for test in test_cases:
          for test_case, expected in test:
            test_fst = normalize_breton_lib.NormalizeBreton(test_case)
            self.assertEqual(test_fst, expected)

if __name__ == '__main__':
    unittest.main()
