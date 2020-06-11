#!/usr/bin/env python

import normalize_breton_lib
from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('string_to_normalize', None, 'the Breton string to normalize')

def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')
  #TODO(azupon): Add the lib functions
  print(normalize_breton_lib.NormalizeBreton(FLAGS.string_to_normalize))
  #print(normalize_breton_lib.BretonSoftMutation(FLAGS.string_to_normalize))
if __name__ == '__main__':
  app.run(main)
