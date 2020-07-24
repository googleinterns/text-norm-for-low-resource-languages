# Lint as: python3
"""Tests for evaluating preprocessing."""

import unittest
from typing import List
import preprocess

class TestPreprocess(unittest.TestCase):
    """Tests for evaluating preprocess.py."""


    def test_preprocess_ud(self):
        'Test loading in a ud data file.'
        infile = "testdata/test_wo_ud_input.txt"
        input_text: List[str] = preprocess.process_data(infile, "ud")
        expected = ("Ndax ku jëkk a jël dakkantal boobu, di Decce Fu Njogu "
                    "FAAL, dañu naan damm na li Kajoor seqante woon ak Jolof, "
                    "ndax Jolof moo nangu woon Kajoor.")
        self.assertEqual(input_text[0], expected)


    def test_preprocess_um(self):
        'Test loading in a um data file.'
        infile = "testdata/test_zu_um_input.txt"
        input_text: List[str] = preprocess.process_data(infile, "um")
        expected = "ubuntu"
        self.assertEqual(input_text[0], expected)


    def test_preprocess_ac(self):
        'Test loading in an ac data file.'
        infile = "testdata/test_mg_ac_input.txt"
        input_text: List[str] = preprocess.process_data(infile, "ac")
        expected = "amin'ny"
        self.assertEqual(input_text[0], expected)


    def test_preprocess_oscar(self):
        'Test loading in an oscar data file.'
        infile = "testdata/test_af_oscar_input.txt"
        input_text: List[str] = preprocess.process_data(infile, "oscar")
        expected = ("Nadat dit duidelik geword het dat die Regering die "
                    "aangeleentheid nie verder sou voer nie, het die "
                    "Volksraad die ANC-regering se miskenning van "
                    "internasionaal-aanvaarde regte en verpligtinge en die "
                    "vergrype teen ons volk, onder die aandag van die "
                    "internasionale gemeenskap gebring.")
        self.assertEqual(input_text[0], expected)


    def test_preprocess_lcc(self):
        'Test loading in an lcc data file.'
        infile = "testdata/test_so_lcc_input.txt"
        input_text: List[str] = preprocess.process_data(infile, "lcc")
        expected = ("Dhamaha iyo madhamaha التام والناقص Falalka "
                    "madhamaha waxay ku jirtaa weerta magaca ah iyadoo ka "
                    "dhigaysa mid waqti cayiman dhacay ama qaab cayiman u "
                    "dhacay, wa xayna u dhexeysaa falalka dhamaha iyo qodobada "
                    """"xarfaha macnayaalka" ((أحرف المعاني)).""")
        self.assertEqual(input_text[0], expected)


    def test_load_missing_file(self):
        'Test loading in a file that does not exist.'
        infile = ""
        try:
            input_text: List[str] = preprocess.process_data(infile, "ud")
        except Exception:
            input_text = None
        expected = None
        self.assertEqual(input_text, expected)


if __name__ == '__main__':
    unittest.main()
