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
    data = glob([
        "testdata/test_sentences.tsv",
        "testdata/test_mg_ac_input.txt",
        "testdata/test_zu_lcc_input.tsv",
        "testdata/test_zu_lcc_expected.txt"
        ]
                )
)

py_test(
    name = "preprocess_test",
    srcs = ["preprocess_test.py"],
    data = glob([
        "testdata/test_wo_ud_input.txt",
        "testdata/test_wo_ud_normalized.txt",
        "testdata/test_zu_um_input.txt",
        "testdata/test_zu_um_normalized.txt",
        "testdata/test_mg_ac_input.txt",
        "testdata/test_af_oscar_input.txt",
        "testdata/test_af_oscar_normalized.txt",
        "testdata/test_so_lcc_input.txt",
        "testdata/test_so_lcc_normalized.txt"
        ]
                )
)
