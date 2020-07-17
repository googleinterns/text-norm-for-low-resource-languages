py_binary(
    name = "normalizer",
    srcs = ["normalizer.py"],
    deps = [":normalizer_lib",],
)

py_library(
    name = "normalizer_lib",
    srcs = ["normalizer_lib.py"],
    deps = [
        "//config:af",
        "//config:am",
        "//config:bm_latn",
        "//config:ha",
        "//config:ig",
        "//config:mg",
        "//config:so",
        "//config:sw",
        "//config:wo",
        "//config:yo",
        "//config:zu",
        "//config:utils"
        ]
)

py_test(
    name = "normalizer_test",
    srcs = ["normalizer_test.py"],
    data = glob(["testdata/test_sentences.tsv"])
)
