def BuildLanguageConfigs(language,
                         extra_data_for_grm_normalizer = [],
                         extra_deps_for_grm_normalizer = []):
  python_library(
            name = "config",
            srcs = [language + ".py"],
            data = extra_data_for_grm_normalizer,
            deps = extra_deps_for_grm_normalizer + [
                ":normalizer_lib",
            ],
   )
)
