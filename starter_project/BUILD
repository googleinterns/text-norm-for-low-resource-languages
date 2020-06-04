py_binary(
    name = "foo",
    srcs = ["foo.py"],
    data = [":transform"],  # a cc_binary which we invoke at run time
    deps = [
        "//pyglib",
        ":foolib",  # a py_library
    ],
)

py_library()

py_test()
