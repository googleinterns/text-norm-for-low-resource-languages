#!/usr/bin/env python

import normalize_breton_lib as norm
from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('string_to_normalize', None, 'the Breton string to normalize')

def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')
  #TODO(azupon): Add the lib functions
  input_text = FLAGS.string_to_normalize
  print("INPUT TEXT:\t\t"+input_text)
  normalized_text = norm.NormalizeBreton(input_text)
  print("NORMALIZED TEXT:\t"+normalized_text)
 # print(norm.NormalizeBreton(FLAGS.string_to_normalize))
 # print(norm.NormalizeBretonSoftMutation(FLAGS.string_to_normalize))
if __name__ == '__main__':
  app.run(main)
