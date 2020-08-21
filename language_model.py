# Lint as: python3
"""Trains an nltk language model."""

import random
import pickle
from typing import List, Tuple
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import Laplace
from absl import app
from absl import flags
from tqdm import tqdm

FLAGS = flags.FLAGS

flags.DEFINE_string('string_to_normalize', None, 'the string to normalize')
flags.DEFINE_string('language', None, 'the language to normalize')
flags.DEFINE_spaceseplist('data_source', None, 'data source to preprocess')
flags.DEFINE_string('pass_valid', "token", 'pass only valid tokens or sentences')
flags.DEFINE_string('experiment', None, 'the normalization experiment to run')


def main(argv):
    """Trains an nltk language model.

    Loads in files of normalized text, partitions them into a train partition
    (3/4 of data) and a test partition (last 1/4 of data). Uses Laplace
    smoothing for unseen ngrams.
    """
    if len(argv) > 1:
        raise app.UsageError("Too many command-line arguments.")

    normalized_data = load_normalized_data(FLAGS.language,
                                           FLAGS.data_source,
                                           FLAGS.pass_valid,
                                           FLAGS.experiment)
    train_partition, test_partition = partition_data(normalized_data)
    train_ngrams, vocab = padded_everygram_pipeline(2, train_partition)
    test_ngrams, _ = padded_everygram_pipeline(2, test_partition)
    language_model = Laplace(2)
    language_model.fit(train_ngrams, vocab)

    avg_perp, count = compute_avg_perplexity(test_ngrams, language_model)
    print("\n----------------------------\n"
          "Language Model Parameters:\n"
          f"\tLanguage={FLAGS.language}\n"
          f"\tData Sources={FLAGS.data_source}\n"
          f"\tPass Valid={FLAGS.pass_valid}\n"
          f"\tExperiment={FLAGS.experiment}\n"
          "----------------------------\n")
    print(f"Average perplexity across {count} ngrams:\t{avg_perp}")


def load_normalized_data(language: str,
                         data_source: str,
                         pass_valid: str,
                         experiment: str
                         ) -> List[List[str]]:
    """Loads one or more files of normalized data.

    Args:
        language: The language of the data.
        data_source: A list of sources of data to load in.
        pass_valid: Whether the whole sentence or just tokens was filtered.
        experiment: The name of the specific experiment being run.

    Returns:
        normalized_data: The normalized data as a list of lists of strings.
    """
    normalized_data = []
    for source in data_source:
        condition: str = ("language=" + language + "_" +
                          "datasource=" + source + "_" +
                          "passvalid=" + pass_valid)
        filename: str = ("output/" + experiment + "/" +
                         condition + "_normalized.p")
        try:
            normalized_data = (normalized_data +
                               pickle.load(open(filename, "rb")))
        except Exception:
            print(f"No normalized data for LANGUAGE={language} "
                  f"from SOURCE={source} for EXPERIMENT={experiment}.")
    returned = []
    for line in normalized_data:
        if line[0] != "<SENTENCE_REJECTED>":
            returned.append(line)
    random.seed(42)
    random.shuffle(returned)
    rejected = len(normalized_data) - len(returned)
    print(f"Loaded {len(normalized_data)} sentences!")
    print(f"Kept {len(returned)} sentences!")
    print(f"Rejected {rejected} sentences ({100*(rejected/len(normalized_data))} %)!")
    return returned


def partition_data(data: List[List[str]]
                   ) -> Tuple[List[List[str]], List[List[str]]]:
    """Partitions data into train and test partitions.

    The train partition consists of 80% of the data.
    The test partition consists of 20% of the data.

    Args:
        data: The normalized data as a list of lists of strings.

    Returns:
        train_partition: The training partition.
        test_partition: The testing partition.
    """
    partition_size = round(len(data)/5)
    train_partition = data[:partition_size*4]
    test_partition = data[partition_size*4:]
    return train_partition, test_partition


def compute_avg_perplexity(test_ngrams, language_model) -> Tuple[float, int]:
    """Computes the average perplexity of all bigrams using Laplace smoothing.

    Args:
        test_ngrams: The ngrams from the testing partition.

    Returns:
        count: The number of ngrams.
        avg_perp: The average perplexity across all ngrams.
    """
    count = 0
    total_perp = 0
    print(f"Computing perplexity of ngrams...")
    for sent in tqdm(test_ngrams):
        for ngram in sent:
            perp = language_model.perplexity([ngram])
            count += 1
            total_perp += perp
    avg_perp = total_perp/count
    return avg_perp, count


if __name__ == "__main__":
    app.run(main)
