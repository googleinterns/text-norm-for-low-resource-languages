# Text Normalization for Low Resource Languages

This repository contains code and data related to the Google open source internship project Text Normalization for Low Resource Languages.

## Project Description

Training data for machine learning models can come from many different sources, which can be of dubious quality. For resource-rich languages like English, there is a lot of data available, so we can afford to throw out the dubious data. For low-resource languages where there is much less data available, we can’t necessarily afford to throw out the dubious data, lest we end up with a training set too small to train a model.

The objective of this project was to study the effects of text normalization and data set quality for a set of low-resource languages of Africa. This involved building a text normalizer using Pynini, a Python library for finite state transducers, and training a language model using the Natural Language Toolkit (NLTK), an open-source Python library for NLP.

## Running the Pipeline

### Language Data

The language-specific config files in `config/` include the paths to the language data files in `language_data/`. The repo does NOT include the data, however. You will need to download it yourself and make sure it is in the right place. The data we used comes from [Universal Dependencies](https://universaldependencies.org/#language-u), the [Leipzig Corpora Collection](https://wortschatz.uni-leipzig.de/en/download), [OSCAR](https://oscar-corpus.com/), and [An Crúbadán](http://crubadan.org/).

### Running the Normalizer

The text normalizer can normalize individual strings or load in a data file and normalize the whole file. The normalizer uses (up to) 5 flags
- `language`:  two-letter flag for the language, e.g. `af`, `mg`; exception is Bambara `bm_latn`
- `data_source`:  flag for the data source, e.g. `ud`, `lcc`, `ac`, `oscar`; not needed if you provide a value for `string_to_normalize`
- `pass_valid`:  whether to filter out individual tokens or sentences; value is `token` or `sentence`
- `experiment`:  name of experimental directory to create and output results to
- `string_to_normalize`:  a specific string to normalize; if you include this, will not preprocess or load any data files (`data_source` flat becomes unnecessary)

To run the normalizer, run 
>`bazel build normalizer && bazel-bin/normalizer --language=LANGUAGE --data_source=DATA_SOURCE --pass_valid=PASS_VALID --experiment=EXPERIMENT --string-to_normalize=STRING`

Remember that `string_to_normalize` is only needed if you don't want to normalize an entire file, and `data_source` is only needed if you _do_ want to normalize an entire file.

If you normalize just a single string, the input, the token-filtered output, and the sentence-filtered output will print to the terminal. If you normalize a file, it will generate three output files in a directory named after the `experiment` flag:
- human readable output consisting of an index, the input text, and the output text in a `.tsv` file
- a pickled list of strings of the input text
- a pickled list of strings of the output text

### Language Model

The language model is written using the Natural Language Toolkit (NLTK).

The language model uses almost the same flags as the text normalizer, only missing `string_to_normalize`. The language model will load in the appropriate pickled file, partition the data, fit the language model, and calculate average perplexity over the ngrams in the test partition. To train and test the language model, run
>`python3 language_model.py --language=LANGUAGE --data_source=DATA_SOURCE --pass_valid=PASS_VALID --experiment=EXPERIMENT`

This will print the total number of sentences in the normalized data, the number of sentences kept, the number of sentences rejected, and the proportion of sentences rejected overall. After fitting the model and calculating average perplexity, it will also print out the total number of ngrams used in testing and the average perplexity across those ngrams.

## Source Code Headers

Every file containing source code must include copyright and license
information. This includes any JS/CSS files that you might be serving out to
browsers. (This is to help well-intentioned people avoid accidental copying that
doesn't comply with the license.)

Apache header:

    Copyright 2020 Google LLC

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
