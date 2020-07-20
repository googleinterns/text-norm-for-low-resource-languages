# Lint as: python3
"""Normalizes text by applying the text normalizer.

Either normalizes the text from a flag, or loads an external file of
sentences to normalize. If it uses the external file, it will write
the sentences that were changed to a new file.
"""
import importlib
from typing import List
from tqdm import tqdm
from absl import app
from absl import flags
import normalizer_lib
import preprocess

FLAGS = flags.FLAGS

flags.DEFINE_string('string_to_normalize', None, 'the string to normalize')
flags.DEFINE_string('language', None, 'the language to normalize')
flags.DEFINE_string('data_source', None, 'data source to preprocess')
flags.DEFINE_string('pass_valid', "token", 'pass only valid tokens or sentences')

def main(argv):
    """Normalizes text by all steps in the text normalizer.

    If given an input string and a language flag, will normalize that string
    using the language's config. If given the language flag and data source
    flag, will normalize the file listed for that data source in the language's
    config file, saving the output to a new tsv file.
    """
    try:
        language = importlib.import_module("config."+FLAGS.language)
    except:
        raise app.UsageError("Needs a value for the language flag.")

    language_library = normalizer_lib.NormalizerLib(FLAGS.language)

    if len(argv) > 1:
        raise app.UsageError("Too many command-line arguments.")

    if FLAGS.string_to_normalize is not None:
        input_text: str = FLAGS.string_to_normalize
        print("TOKEN_BASED:\t"+
              language_library.token_normalizer(FLAGS.string_to_normalize))
        print("SENTENCE_BASED:\t"+
              language_library.sentence_normalizer(FLAGS.string_to_normalize))
    else:
        data_source: str = FLAGS.data_source
        if data_source == "ud":
            infile = language.UD
        elif data_source == "um":
            infile = language.UM
        elif data_source == "ac":
            infile = language.AC
        elif data_source == "oscar":
            infile = language.OSCAR
        elif data_source == "lcc":
            infile = language.LCC
        try:
            input_text: List[str] = preprocess.process_data(infile, FLAGS.data_source)
        except Exception:
            print("No data file from '{}' for '{}'".format(data_source, FLAGS.language))
            return
        outfile: str = ("./output/"+
                        FLAGS.language+"_"+
                        data_source+"_"+
                        FLAGS.pass_valid+"_"+
                        "normalized.tsv")

        total_sentences: int = 0
        changed_sentences: int = 0

        output_file = open(outfile, "w")
        output_file.write("SENTENCE_ID\tSENTENCE_TEXT\tNORMALIZED_TEXT\n")

        i = 0
        for line in tqdm(input_text):
            total_sentences += 1
            sentence_id: str = str(i)
            sentence_text: str = line
            if FLAGS.pass_valid == "token":
                normalized_text: str = language_library.token_normalizer(
                    sentence_text)
            elif FLAGS.pass_valid == "sentence":
                normalized_text: str = language_library.sentence_normalizer(
                    sentence_text)
            if normalized_text != sentence_text.strip().lower():
                changed_sentences += 1
                newline = (sentence_id+"\t"+
                           sentence_text.strip().lower()+"\t"+
                           normalized_text+"\n")
                output_file.write(newline)
            i += 1
        print("Changed {} out of {} sentences!".format(
            changed_sentences, total_sentences))


if __name__ == '__main__':
    app.run(main)
