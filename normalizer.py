# Lint as: python3
"""Normalizes text by applying the text normalizer.

Either normalizes the text from a flag, or loads an external file of
sentences to normalize. If it uses the external file, it will write
the sentences that were changed to a new file.
"""
import os
import importlib
from typing import List
import pickle
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
flags.DEFINE_string('experiment', None, 'the normalization experiment to run')

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

    norm = normalizer_lib.NormalizerLib(FLAGS.language)

    if len(argv) > 1:
        raise app.UsageError("Too many command-line arguments.")

    if FLAGS.string_to_normalize is not None:
        input_text: str = FLAGS.string_to_normalize
        print("TOKEN_BASED:\t"+
              norm.token_normalizer(FLAGS.string_to_normalize))
        print("SENTENCE_BASED:\t"+
              norm.sentence_normalizer(FLAGS.string_to_normalize))
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
            print(f"No data file from '{data_source}' for '{FLAGS.language}'.")
            return

        experiment_dir: str = "./output/" + FLAGS.experiment
        if not os.path.exists(experiment_dir):
            os.makedirs(experiment_dir)
        condition: str = ("language=" + FLAGS.language + "_" +
                          "datasource=" + data_source + "_" +
                          "passvalid=" + FLAGS.pass_valid)
        outfile_human_readable: str = ("./output/" +
                                       FLAGS.experiment + "/" +
                                       condition + "_" +
                                       "humanreadable.tsv")
        outfile_unnormalized: str = ("./output/" +
                                     FLAGS.experiment + "/" +
                                     condition + "_" +
                                     "unnormalized.p")
        outfile_normalized: str = ("./output/" +
                                   FLAGS.experiment + "/" +
                                   condition + "_" +
                                   "normalized.p")

        unnormalized_data_for_lm = []
        normalized_data_for_lm = []

        human_readable_output = open(outfile_human_readable, "w")
        human_readable_output.write("SENTENCE_ID\tUNNORMALIZED_TEXT\tNORMALIZED_TEXT\n")

        i = 0
        for line in tqdm(input_text):
            sentence_id: str = str(i)
            sentence_text: str = line.strip()
            if FLAGS.pass_valid == "token":
                normalized_text: str = norm.token_normalizer(
                    sentence_text)
            elif FLAGS.pass_valid == "sentence":
                normalized_text: str = norm.sentence_normalizer(
                    sentence_text)
            newline = (sentence_id + "\t" +
                       sentence_text + "\t" +
                       normalized_text + "\n")
            human_readable_output.write(newline)
            unnormalized_data_for_lm.append(sentence_text.split(" "))
            normalized_data_for_lm.append(normalized_text.split(" "))
            i += 1
            # files pickled here after each line so there's data in case the
            # process ends before normalizing the entire data file
            pickle.dump(unnormalized_data_for_lm, open(outfile_unnormalized, "wb"))
            pickle.dump(normalized_data_for_lm, open(outfile_normalized, "wb"))


if __name__ == '__main__':
    app.run(main)
