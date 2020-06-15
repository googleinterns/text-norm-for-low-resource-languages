#!/usr/bin/env python

import normalize_breton_lib as norm
from absl import app
from absl import flags
import re


FLAGS = flags.FLAGS

flags.DEFINE_string('string_to_normalize', None, 'the Breton string to normalize')

FILENAME = "./bre_wikipedia_2016_100K/bre_wikipedia_2016_100K-sentences.txt"

with open(FILENAME) as f:
  breton_sentences = f.readlines()
#print(breton_sentences[:5])

def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')
  #TODO(azupon): Add the lib functions
  for line in breton_sentences[:20]:
    sentence_id, sentence_text = line.split("\t")[0], line.split("\t")[1]
  #  input_text = FLAGS.string_to_normalize
    remove_special_characters = re.sub(r"[^0-9a-zA-Z\s\-'’\u00C0-\u00FF]+", "", sentence_text)
    preprocessed_text = re.sub(r"[^\w\s'’-]","",sentence_text).strip()
#    normalized_text = norm.NormalizeBreton(preprocessed_text)
    print("SENTENCE:\t\t"+sentence_id)
    print("ORIGINAL TEXT:\t\t"+sentence_text.strip())
    print("PREPROCESSED TEXT:\t"+preprocessed_text)
    normalized_text = norm.NormalizeBreton(preprocessed_text)
    print("NORMALIZED TEXT:\t"+normalized_text)
   # print(norm.NormalizeBreton(FLAGS.string_to_normalize))
   # print(norm.NormalizeBretonSoftMutation(FLAGS.string_to_normalize))
if __name__ == '__main__':
  app.run(main)
