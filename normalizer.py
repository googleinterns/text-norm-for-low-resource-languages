# Lint as: python3
"""Normalizes text by applying the text normalizer.

Either normalizes the text from a flag, or loads an external file of
sentences to normalize. If it uses the external file, it will write
the sentences that were changed to a new file.
"""

from absl import app
from absl import flags
import normalizer_lib

FLAGS = flags.FLAGS

flags.DEFINE_string('string_to_normalize', None, 'the string to normalize')

#INFILE: str = "./testdata/test-sentences.txt"
#OUTFILE: str = "normalized_sentences.tsv"

#with open(INFILE) as f:
#    SENTENCES = f.readlines()


def main(argv):
    """Normalizes text by all steps in the text normalizer."""

    if len(argv) > 1:
        raise app.UsageError("Too many command-line arguments.")

    if FLAGS.string_to_normalize is not None:
        input_text: str = FLAGS.string_to_normalize
        print(normalizer_lib.normalize_everything(FLAGS.string_to_normalize))

    else:
        total_sentences: int = 0
        changed_sentences: int = 0

        output_file = open(OUTFILE, "w")
        output_file.write("SENTENCE_ID\tSENTENCE_TEXT\tNORMALIZED_TEXT\n")

        for line in SENTENCES:
            total_sentences += 1
            sentence_id: str = line.split("\t")[0]
            sentence_text: str = line.split("\t")[1]
            normalized_text: str = normalizer_lib.normalize_everything(sentence_text)

            if normalized_text != sentence_text.strip().lower():
                changed_sentences += 1
                newline = sentence_id+"\t"+sentence_text.strip().lower()+"\t"+normalized_text+"\n"
                output_file.write(newline)

        print("Changed {} out of {} sentences!".format(changed_sentences, total_sentences))


if __name__ == '__main__':
    app.run(main)
