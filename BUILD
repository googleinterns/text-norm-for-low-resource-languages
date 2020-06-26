py_binary(
    name = "normalizer",
    srcs = ["normalizer.py"],
    deps = [":normalizer_lib",],
)

py_library(
    name = "normalizer_lib",
    srcs = ["normalizer_lib.py"]
)

py_test(
    name = "normalizer_test",
    srcs = ["normalizer_test.py"],
    data = glob(["testdata/test_sentences.tsv"])
)
