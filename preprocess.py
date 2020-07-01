# Lint as: python3
"""TODO(azupon): DO NOT SUBMIT without one-line documentation for preprocess.

TODO(azupon): DO NOT SUBMIT without a detailed description of preprocess.
"""

from absl import app
from absl import flags
from typing import List
import re
import unicodedata

FLAGS = flags.FLAGS


def process_UD_data(ud_file: str) -> List[str]:
    "Processes UD conllu file into list of strings for normalization."
    with open(ud_file) as infile:
        ud_lines = infile.readlines()
    UD_SENTENCES: List[str] = []
    for line in ud_lines:
        if "# text" in line:
            SENTENCE:str = unicodedata.normalize("NFC", line[9:].strip())
            LSB = re.sub("\[", "\\[", SENTENCE)
            RSB = re.sub("\]", "\\]", LSB)
            UD_SENTENCES.append(RSB)
        else:
            continue
    return UD_SENTENCES

def main(argv):
    if len(argv) > 1:
        raise app.UsageError('Too many command-line arguments.')

if __name__ == '__main__':
    app.run(main)
