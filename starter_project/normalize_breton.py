#!/usr/bin/env python

import normalize_breton_lib as norm
from absl import app
from absl import flags
import re
from tqdm import tqdm

FLAGS = flags.FLAGS

flags.DEFINE_string('string_to_normalize', None, 'the Breton string to normalize')

INFILE: str = "./bre_wikipedia_2016_100K/bre_wikipedia_2016_100K-sentences.txt"
OUTFILE: str = "./bre_normalized_sentences"

with open(INFILE) as f:
  breton_sentences = f.readlines()

def main(argv):
  """Normalize the Breton text by applying mutations and save a .tsv file of the changed sentences."""

  total_sentences: int = 0
  changed_sentences: int = 0

  output_file: file = open(OUTFILE, "w")
  output_file.write("SENTENCE_ID\tSENTENCE_TEXT\tNORMALIZED_TEXT\n")

  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  for line in tqdm(breton_sentences):
    total_sentences += 1
    sentence_id: str = line.split("\t")[0]
    sentence_text: str = line.split("\t")[1]
#    input_text: str = FLAGS.string_to_normalize
#    print(norm.NormalizeBreton(FLAGS.string_to_normalize))
#    print(norm.NormalizeBretonSoftMutation(FLAGS.string_to_normalize))
    normalized_text: str = norm.NormalizeBreton(sentence_text)

    if normalized_text != sentence_text.strip().lower():
      changed_sentences += 1
      newline = sentence_id+"\t"+sentence_text.strip().lower()+"\t"+normalized_text+"\n"
      output_file.write(newline)
#      print(sentence_id)
#      print(sentence_text.strip().lower())
#      print(normalized_text)

  print("Changed {} out of {} sentences!".format(changed_sentences, total_sentences))

if __name__ == '__main__':
  app.run(main)

