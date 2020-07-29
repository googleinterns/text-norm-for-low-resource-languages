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
    about the token, lemma, part of speech, and dependency syntax. For example:

        # sent_id = GEN_1.1
        # text = Ní ìbẹ̀rẹ̀ ohun gbogbo Ọlọ́run dá àwọn ọ̀run àti ayé.
        # text_en = In the beginning God created the heaven and the earth.
        1       Ní      ní      ADP     _       _       2       case    _       Gloss=in|Ref=GEN_1.1
        2       ìbẹ̀rẹ̀   ìbẹ̀rẹ̀   NOUN    _       _       6       obl     _       Gloss=beginning|Ref=GEN_1.1
        3       ohun    ohun    NOUN    _       _       5       nmod    _       Gloss=things|Ref=GEN_1.1
        4       gbogbo  gbogbo  DET     _       _       5       det     _       Gloss=all|Ref=GEN_1.1
        5       Ọlọ́run  ọlọ́run  NOUN    _       _       6       nsubj   _       Gloss=god|Ref=GEN_1.1
        6       dá      dá      VERB    _       _       0       root    _       Gloss=made|Ref=GEN_1.1
        7       àwọn    àwọn    DET     _       _       8       det     _       Gloss=the|Ref=GEN_1.1
        8       ọ̀run    ọ̀run    NOUN    _       _       6       obj     _       Gloss=heaven|Ref=GEN_1.1
        9       àti     àti     CCONJ   _       _       10      cc      _       Gloss=and|Ref=GEN_1.1
        10      ayé     ayé     NOUN    _       _       8       conj    _       Gloss=earth|Ref=GEN_1.1|SpaceAfter=No
        11      .       .       PUNCT   _       _       6       punct   _       Gloss=.|Ref=GEN_1.1


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
        if "# text =" in line:
            text: str = line.split(" text = ")[1]
            sentence: str = substitute_brackets(text)
            print(sentence)
            ud_sentences.append(sentence)
        else:
            continue
    print(ud_sentences)
    return ud_sentences


def process_um_data(um_file: str) -> List[str]:
    """Processes UniMorph file into list of strings for normalization.

    UM data format is the word lemma, followed by a tab, followed by
    the inflected form of the word, followed by another tab, followed by
    fine-grained morphological information. For example:

        ubuntu  wobuntu N;SG;PSSB1
        ubuntu  elobuntu  N;SG;LGSPEC1;PSSB5
        ubuntu  yobuntu N;SG;PSSB4
        ubuntu  obobuntu  N;SG;LGSPEC1;PSSB14

    Args:
        um_file: The um data file to process.

    Returns:
        A list of processed words.
    """
    um_lines = read_file_as_lines(um_file)
    um_words: List[str] = []
    for line in um_lines:
        text: str = line.strip().split("\t")[0]
        word: str = substitute_brackets(text)
        um_words.append(word)
    return um_words


def process_ancrubadan_data(ac_file: str) -> List[str]:
    """Processes An Crubadan file into list of strings for normalization.

    An Crubadan data format is the word, followed by a space, followed by
    the total count of that word in the corpora that were crawled. For example:

        die 188641
        en 83603
        van 81295
        het 64692
        'n 62512

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
    does not separate these into separate sentences. For example:

        Ìpínlẹ̀ Ẹdó jẹ́ ìkan nínú àwọn ìpínlẹ̀ mẹ́rìndínlógójì ní orílẹ̀ èdè Nàìjíríà. Ó sàgbè pẹ̀lú àríwá àti ìwọ̀ oòrùn ìpínlẹ̀ Kogi, àgbè pẹ̀lú gúúsù ìpínlẹ̀ Delta àti ìlà-oòrùn ìpínlẹ̀ Ondo.

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

    LCC data format is the sentence index, followed by spaces,
    followed by the sentence text. For example:

        634     Annagase Mu’miniin dhab ah ma nahay?

    Args:
        lcc_file: The lcc data file to process.

    Returns:
        A list of processed sentences.
    """
    lcc_lines = read_file_as_lines(lcc_file)
    lcc_sentences: List[str] = []
    for line in lcc_lines:
        text: str = re.sub(r"^[0-9]+\s+", "", line)
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
    sub_left_bracket = re.sub(r"\[", "(", string.strip())
    sub_right_bracket = re.sub(r"\]", ")", sub_left_bracket)
    return sub_right_bracket


def main(argv):
    if len(argv) > 1:
        raise app.UsageError('Too many command-line arguments.')

if __name__ == '__main__':
    app.run(main)
