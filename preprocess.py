# Lint as: python3
"""Methods to preprocess data from different sources for text normalization.
"""

import re
from typing import List
from absl import app
from absl import flags

FLAGS = flags.FLAGS


def process_ud_data(ud_file: str) -> List[str]:
    "Processes UD conllu file into list of strings for normalization."
    with open(ud_file) as infile:
        ud_lines = infile.readlines()
    ud_sentences: List[str] = []
    for line in ud_lines:
        if "# text" in line:
            sentence: str = line[9:].strip()
            sub_left_bracket = re.sub(r"\[", "\\[", sentence)
            sub_right_bracket = re.sub(r"\]", "\\]", sub_left_bracket)
            ud_sentences.append(sub_right_bracket)
        else:
            continue
    return ud_sentences


def process_um_data(um_file: str) -> List[str]:
    "Processes UniMorph file into list of strings for normalization."
    raise NotImplementedError


def process_ancrubadan_data(ac_file: str) -> List[str]:
    "Processes An Crubadan file into list of strings for normalization."
    raise NotImplementedError


def process_oscar_data(oscar_file: str) -> List[str]:
    "Processes OSCAR file into list of strings for normalization."
    raise NotImplementedError


def process_lcc_data(lcc_file: str) -> List[str]:
    "Processes Leipzig Corpora Collection file for normalization."
    raise NotImplementedError


def main(argv):
    if len(argv) > 1:
        raise app.UsageError('Too many command-line arguments.')

if __name__ == '__main__':
    app.run(main)
