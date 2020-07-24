#!/bin/bash
# For loop to normalize files from each data source for each language.

for language in af am bm_latn ha ig mg so sw wo yo zu
do

    for data_source in ud um ac oscar lcc
    do
        bazel build normalizer && bazel-bin/normalizer --language=$language --data_source=$data_source
    done

done
