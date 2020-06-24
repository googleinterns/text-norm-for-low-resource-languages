#!/usr/bin/env python
"""Normalizes text by applying different consonant mutations.

Either normalizes the text from a flag, or loads an external file of
sentences from Breton Wikipedia to normalize. If it uses the external
file, it will write the sentences that were changed to a new file.
"""

from absl import app
from absl import flags
import normalize_breton_lib

FLAGS = flags.FLAGS

flags.DEFINE_string('string_to_normalize', None, 'the Breton string to normalize')

INFILE: str = "./bre_wikipedia_2016_100K/bre_wikipedia_2016_100K-sentences.txt"
OUTFILE: str = "bre_normalized_sentences.tsv"

with open(INFILE) as f:
    BRETON_SENTENCES = f.readlines()

def main(argv):
    """Normalize text by applying initial consonant mutations."""

    if len(argv) > 1:
        raise app.UsageError("Too many command-line arguments.")

    if FLAGS.string_to_normalize is not None:
        input_text: str = FLAGS.string_to_normalize
        print(normalize_breton_lib.normalize_breton(FLAGS.string_to_normalize))

    else:
        total_sentences: int = 0
        changed_sentences: int = 0

        output_file = open(OUTFILE, "w")
        output_file.write("SENTENCE_ID\tSENTENCE_TEXT\tNORMALIZED_TEXT\n")

        for line in BRETON_SENTENCES:
            total_sentences += 1
            sentence_id: str = line.split("\t")[0]
            sentence_text: str = line.split("\t")[1]
            normalized_text: str = normalize_breton_lib.normalize_breton(sentence_text)

            if normalized_text != sentence_text.strip().lower():
                changed_sentences += 1
                newline = sentence_id+"\t"+sentence_text.strip().lower()+"\t"+normalized_text+"\n"
                output_file.write(newline)

        print("Changed {} out of {} sentences!".format(changed_sentences, total_sentences))

if __name__ == '__main__':
    app.run(main)
