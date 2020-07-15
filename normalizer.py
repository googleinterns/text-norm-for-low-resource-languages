# Lint as: python3
"""Normalizes text by applying the text normalizer.

Either normalizes the text from a flag, or loads an external file of
sentences to normalize. If it uses the external file, it will write
the sentences that were changed to a new file.
"""
from typing import List
from tqdm import tqdm
from absl import app
from absl import flags
import normalizer_lib
import preprocess
import importlib

FLAGS = flags.FLAGS

flags.DEFINE_string('string_to_normalize', None, 'the string to normalize')
flags.DEFINE_string('language', None, 'the language to normalize')
flags.DEFINE_string('data_source', None, 'data source to preprocess')


def main(argv):
    """Normalizes text by all steps in the text normalizer."""

    LANGUAGE = importlib.import_module("config."+FLAGS.language)
#    DATA_SOURCE: str = FLAGS.data_source
    # TODO: find a better way of getting this from the configs
#    if DATA_SOURCE == "ud":
#        INFILE = LANGUAGE.ud
#    elif DATA_SOURCE == "um":
#        INFILE = LANGUAGE.um
#    elif DATA_SOURCE == "ac":
#        INFILE = LANGUAGE.ac
#    elif DATA_SOURCE == "lcc":
#        INFILE = LANGUAGE.lcc
#    try:
#        INPUT_TEXT: List[str] = preprocess.process_data(INFILE, FLAGS.data_source)
#    except:
#        print("No data file from '{}' for '{}'".format(DATA_SOURCE, FLAGS.language))
#        return
#    OUTFILE: str = "./output/"+FLAGS.language+"_"+DATA_SOURCE+"_"+"normalized.tsv"

 #   print("LANGUAGE:\t"+FLAGS.language)
 #   print("DATA_SOURCE:\t"+DATA_SOURCE)
 #   print("INFILE:\t"+INFILE)
    if len(argv) > 1:
        raise app.UsageError("Too many command-line arguments.")

    if FLAGS.string_to_normalize is not None:
        input_text: str = FLAGS.string_to_normalize
        print(normalizer_lib.normalize_everything(FLAGS.string_to_normalize))

    else:
        DATA_SOURCE: str = FLAGS.data_source
        # TODO: find a better way of getting this from the configs
        if DATA_SOURCE == "ud":
            INFILE = LANGUAGE.ud
        elif DATA_SOURCE == "um":
            INFILE = LANGUAGE.um
        elif DATA_SOURCE == "ac":
            INFILE = LANGUAGE.ac
        elif DATA_SOURCE == "lcc":
            INFILE = LANGUAGE.lcc
        try:
            INPUT_TEXT: List[str] = preprocess.process_data(INFILE, FLAGS.data_source)
        except:
            print("No data file from '{}' for '{}'".format(DATA_SOURCE, FLAGS.language))
            return
        OUTFILE: str = "./output/"+FLAGS.language+"_"+DATA_SOURCE+"_"+"normalized.tsv"

        total_sentences: int = 0
        changed_sentences: int = 0

        output_file = open(OUTFILE, "w")
        output_file.write("SENTENCE_ID\tSENTENCE_TEXT\tNORMALIZED_TEXT\n")

        i = 0
        for line in tqdm(INPUT_TEXT):
            total_sentences += 1
            sentence_id: str = str(i)
            sentence_text: str = line
            normalized_text: str = normalizer_lib.normalize_everything(sentence_text)

            if normalized_text != sentence_text.strip().lower():
                changed_sentences += 1
                newline = sentence_id+"\t"+sentence_text.strip().lower()+"\t"+normalized_text+"\n"
                output_file.write(newline)
            i += 1
        print("Changed {} out of {} sentences!".format(changed_sentences, total_sentences))


if __name__ == '__main__':
    app.run(main)
