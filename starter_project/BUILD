py_binary(
    name = "normalize_breton",
    srcs = ["normalize_breton.py"],
    deps = [":normalize_breton_lib",],
)

py_library(
    name = "normalize_breton_lib",
    srcs = ["normalize_breton_lib.py"]
)

py_test(
    name = "normalize_breton_test",
    srcs = ["normalize_breton_test.py"],
    data = glob(["testdata/bre_normalized_sentences.tsv"])
)
