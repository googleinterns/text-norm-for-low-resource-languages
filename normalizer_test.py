# Lint as: python3
"""Tests for evaluating text normalizer."""

import unittest
import normalizer_lib

norm = normalizer_lib.NormalizerLib("af")

class TestNormalizer(unittest.TestCase):
    """Tests for evaluating text normalizer."""

    #norm = normalizer_lib.NormalizerLib("af")

    def test_token_normalizer(self):
        'Test the output of normalizer.'
        raise NotImplementedError
        with open("testdata/normalized_sentences.tsv", "r") as test_file:
            test_cases = test_file.readlines()[1:]
        for sentence in test_cases:
            with self.subTest(sentence=sentence):
                test_case = sentence.strip().split("\t")[1]
                expected = sentence.strip().split("\t")[2]
                test_fst = normalizer_lib.token_normalizer(test_case)
                self.assertEqual(test_fst, expected)


    def test_sentence_normalizer(self):
        'Test the output of normalizer.'
        raise NotImplementedError
        with open("testdata/normalized_sentences.tsv", "r") as test_file:
            test_cases = test_file.readlines()[1:]
        for sentence in test_cases:
            with self.subTest(sentence=sentence):
                test_case = sentence.strip().split("\t")[1]
                expected = sentence.strip().split("\t")[2]
                test_fst = normalizer_lib.sentence_normalizer(test_case)
                self.assertEqual(test_fst, expected)


    def test_remove_extra_whitespace(self):
        'Test removing extra whitespace.'
        for test in [(("hi       there", "hi there"),
                      ("my friend    ", "my friend "),
                      ("   the sun", " the sun"),
                      ("   all   the   spaces   ", " all the spaces "))]:
            for test_case, expected in test:
                with self.subTest(test_case=test_case):
                    normalized_text = norm.remove_extra_whitespace(test_case).string()
#                    normalized_text = (test_case @
#                                       normalizer_lib.REMOVE_EXTRA_WHITESPACE
#                                       ).string()
                    self.assertEqual(normalized_text, expected)


    def test_separate_punctuation(self):
        'Test separating punctuation from tokens.'
        for test in [(("hello, friend",
                       "hello , friend"),
                      ("the end.",
                       "the end ."),
                      ('"what',
                       '" what'),
                      ('"who, he asked, left?"',
                       '" who , he asked , left ? "'),
                      ("don't separate apostrophes",
                       "don't separate apostrophes"),
                      ("initial 'apostrophe",
                       "initial 'apostrophe"),
                      ("final' apostrophe",
                       "final ' apostrophe"),
                      ("keep ice-cream together",
                       "keep ice-cream together"),
                      ("50,000", "50,000"),
                      ("google.com", "google.com"),
                      ("12:25", "12:25"))]:
            for test_case, expected in test:
                with self.subTest(test_case=test_case):
                    normalized_text = norm.detach_punctuation(test_case).string()
#                    normalized_text = (test_case @
#                                       normalizer_lib.SEPARATE_PUNCTUATION
#                                       ).string()
                    self.assertEqual(normalized_text, expected)


    def test_delete_freestanding_punctuation(self):
        'Test deleting freestanding punctuation.'
        for test in [(("hello , friend", "hello  friend"),
                      ("the end .", "the end "),
                      ('" what', ' what'),
                      ('" who , he asked , left ? "', ' who  he asked  left  '))]:
            for test_case, expected in test:
                with self.subTest(test_case=test_case):
                    normalized_text = norm.delete_freestanding_punctuation(test_case).string()
#                    normalized_text = (test_case @
#                                       normalizer_lib.DELETE_FREESTANDING_PUNCTUATION
#                                       ).string()
                    self.assertEqual(normalized_text, expected)


    def test_pass_only_valid(self):
        'Test deleting tokens not in language.'
        for test in [(("hello, товарищ", "hello, <UNK>"),
                      ("ABCÄÖÜß", "<UNK>"),
                      ("Где мой dog?", "<UNK> <UNK> dog?"))]:
            for test_case, expected in test:
                with self.subTest(test_case=test_case):
                    normalized_text = norm.pass_only_valid_tokens(test_case)
#                    normalized_text = normalizer_lib.pass_only_valid_tokens(test_case)
                    self.assertEqual(normalized_text, expected)

if __name__ == '__main__':
    unittest.main()
