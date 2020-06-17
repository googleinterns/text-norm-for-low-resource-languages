#!/usr/bin/env python
"""Library of FST rewrite rules to handle Celtic initial consonant mutations."""

from pynini import *
from MutationHandler import *

language = "breton"
mutation_handler = CelticMutationHandler(language)

GRAPHEMES = mutation_handler.GRAPHEMES

SOFT_TRIGGERS = mutation_handler.soft_triggers
HARD_TRIGGERS = mutation_handler.hard_triggers
SPIRANT_TRIGGERS = mutation_handler.spirant_triggers
MIXED_TRIGGERS = mutation_handler.mixed_triggers
NASAL_TRIGGERS = mutation_handler.nasal_triggers
LENITION_TRIGGERS = mutation_handler.lenition_triggers
ECLIPSIS_TRIGGERS = mutation_handler.eclipsis_triggers

SOFT_MUTATION = mutation_handler.soft_map
HARD_MUTATION = mutation_handler.hard_map
SPIRANT_MUTATION = mutation_handler.spirant_map
MIXED_MUTATION = mutation_handler.mixed_map
NASAL_MUTATION = mutation_handler.nasal_map
LENITION_MUTATION = mutation_handler.lenition_map
ECLIPSIS_MUTATION = mutation_handler.eclipsis_map

SPACE = " "
sigma_star = mutation_handler.sigma_star

PREPROCESS = mutation_handler.preprocessing
POSTPROCESS = mutation_handler.postprocessing

DO_SOFT_MUTATION = cdrewrite(
    SOFT_MUTATION,
    union(SPACE, "[BOS]") + SOFT_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    sigma_star)
DO_HARD_MUTATION = cdrewrite(
    HARD_MUTATION,
    union(SPACE, "[BOS]") + HARD_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    sigma_star)
DO_SPIRANT_MUTATION = cdrewrite(
    SPIRANT_MUTATION,
    union(SPACE, "[BOS]") + SPIRANT_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    sigma_star)
DO_MIXED_MUTATION = cdrewrite(
    MIXED_MUTATION,
    union(SPACE, "[BOS]") + MIXED_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    sigma_star)
DO_NASAL_MUTATION = cdrewrite(
    NASAL_MUTATION,
    union(SPACE, "[BOS]") + NASAL_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    sigma_star)
DO_LENITION = cdrewrite(
    LENITION_MUTATION,
    union(SPACE, "[BOS]") + LENITION_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    sigma_star)
DO_ECLIPSIS = cdrewrite(
    ECLIPSIS_MUTATION,
    union(SPACE, "[BOS]") + ECLIPSIS_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    sigma_star)

mutation_dict = {
                 "soft":
                      DO_SOFT_MUTATION,
                  "hard":
                      DO_HARD_MUTATION,
                  "spirant":
                      DO_SPIRANT_MUTATION,
                  "mixed":
                      DO_MIXED_MUTATION,
                  "nasal":
                      DO_NASAL_MUTATION,
                  "lenition":
                      DO_LENITION,
                  "eclipsis":
                      DO_ECLIPSIS,
                    }

DO_PREPROCESSING = cdrewrite(
    PREPROCESS,
    union(SPACE, "[BOS]"),
    union(GRAPHEMES, SPACE),
    sigma_star)

DO_POSTPROCESSING = cdrewrite(
    POSTPROCESS,
    union(SPACE, "[BOS]"),
    union(GRAPHEMES, SPACE),
    sigma_star)


def preprocess(string: str) -> str:
    """Preprocess the string before normalization."""
    return compose(string.strip().lower(), DO_PREPROCESSING).string()


def postprocess(string: str) -> str:
    """Postprocess the string after normalization."""
    return compose(string, DO_POSTPROCESSING).string()


def apply_mutation(string: str, mutation: str) -> str:
    """Applies a single mutation to a string."""
    apply_mutation = compose(string, mutation_dict.get(mutation)).string()
    return apply_mutation


def NormalizeBreton(breton_string: str) -> str:
    """Applies Breton mutations."""
    preprocessed_string = preprocess(breton_string)
    apply_soft_mutation = apply_mutation(preprocessed_string, "soft")
    apply_hard_mutation = apply_mutation(apply_soft_mutation, "hard")
    apply_spirant_mutation = apply_mutation(apply_hard_mutation, "spirant")
    postprocessed_string = postprocess(apply_spirant_mutation)
    return postprocessed_string


def NormalizeWelsh(welsh_string: str) -> str:
    """Applies Welsh mutations."""
    preprocessed_string = preprocess(welsh_string)
    apply_soft_mutation = apply_mutation(preprocessed_string, "soft")
    apply_nasal_mutation = apply_mutation(apply_soft_mutation, "nasal")
    apply_spirant_mutation = apply_mutation(apply_nasal_mutation, "spirant")
    postprocessed_string = postprocess(apply_spirant_mutation)
    return postprocessed_string

