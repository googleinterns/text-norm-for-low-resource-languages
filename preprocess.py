# Lint as: python3
"Methods to preprocess data from different sources for text normalization."

import re
from typing import List
from absl import app


def process_data(data_file: str, data_source: str) -> List[str]:
    """Processes data into list of strings depending on the data source.

    Args:
        data_file: The path to the data file.
        data_source: Which corpus the data comes from.

    Returns:
        List of lines/sentences processed based on the data source.

    Raises:
        KeyError if you don't tell it which data source to use.
    """
    if data_source == "ud":
        return process_ud_data(data_file)
    elif data_source == "um":
        return process_um_data(data_file)
    elif data_source == "ac":
        return process_ancrubadan_data(data_file)
    elif data_source == "oscar":
        return process_oscar_data(data_file)
    elif data_source == "lcc":
        return process_lcc_data(data_file)
    print("Pick a data source!")
    raise Exception


def process_ud_data(ud_file: str) -> List[str]:
    """Processes UD conllu file into list of strings for normalization.

    UD data format follows the CONLL data format, where each sentence includes
    metadata and each token is on a separate line. Each line includes info
    about the token, lemma, part of speech, and dependency syntax. For this
    function we only care about the token.

    Args:
        ud_file: The ud data file to process.

    Returns:
        A list of processed sentences.
    """
    ud_lines: List[str] = read_file_as_lines(ud_file)
    with open(ud_file) as infile:
        ud_lines = infile.readlines()
    ud_sentences: List[str] = []
    for line in ud_lines:
        if "# text" in line:
            text: str = line.split(" text = ")[1]
            sentence: str = substitute_brackets(text)
            ud_sentences.append(sentence)
        else:
            continue
    return ud_sentences


def process_um_data(um_file: str) -> List[str]:
    """Processes UniMorph file into list of strings for normalization.

    UM data format is the word lemma, followed by a tab, followed by
    the inflected form of the word, followed by another tab, followed by
    fine-grained morphological information."""
    raise NotImplementedError


def process_ancrubadan_data(ac_file: str) -> List[str]:
    """Processes An Crubadan file into list of strings for normalization.

    An Crubadan data format is the word, followed by a space, followed by
    the totalcount of that word in the corpora that were crawled.

    Args:
        ac_file: The ac data file to process.

    Returns:
        A list of processed words.
    """
    ac_lines = read_file_as_lines(ac_file)
    ac_words: List[str] = []
    for line in ac_lines:
        text: str = line.split(" ")[0]
        word: str = substitute_brackets(text)
        ac_words.append(word)
    return ac_words


def process_oscar_data(oscar_file: str) -> List[str]:
    """Processes OSCAR file into list of strings for normalization.

    OSCAR data format is one (or more) sentences per line. This processing
    does not separate these into separate sentences.

    Args:
        ac_file: The ac data file to process.

    Returns:
        A list of processed strings consisting of one or more sentences.
    """
    oscar_lines = read_file_as_lines(oscar_file)
    oscar_strings: List[str] = []
    for line in oscar_lines:
        sentence: str = substitute_brackets(line)
        oscar_strings.append(sentence)
    return oscar_strings


def process_lcc_data(lcc_file: str) -> List[str]:
    """Processes Leipzig Corpora Collection file for normalization.

    LCC data format is the sentence index, followed by a tab,
    followed by the sentence text.

    Args:
        lcc_file: The lcc data file to process.

    Returns:
        A list of processed sentences.
    """
    lcc_lines = read_file_as_lines(lcc_file)
    lcc_sentences: List[str] = []
    for line in lcc_lines:
        text: str = line.strip().split("\t")[1]
        sentence: str = substitute_brackets(text)
        lcc_sentences.append(sentence)
    return lcc_sentences


def read_file_as_lines(filename: str) -> List[str]:
    """Reads in filename as list of lines.

    Args:
        filename: The path of the filename to read in.

    Returns: A list of strings.
    """
    with open(filename) as infile:
        file_lines = infile.readlines()
    return file_lines


def substitute_brackets(string: str) -> str:
    """Substitutes square brackets to work in Pynini.

    Args:
        string: A line from the corpus (one or more sentences).

    Returns: The same line with square brackets escaped by slashes.
    """
    sub_left_bracket = re.sub(r"\[", "\\[", string.strip())
    sub_right_bracket = re.sub(r"\]", "\\]", sub_left_bracket)
    return sub_right_bracket


def main(argv):
    if len(argv) > 1:
        raise app.UsageError('Too many command-line arguments.')

if __name__ == '__main__':
    app.run(main)
