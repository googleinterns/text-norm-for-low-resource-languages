#!/usr/bin/env python
"""Library of FST rewrite rules to handle Celtic initial consonant mutations."""

from pynini import *
from MutationHandler import CelticMutationHandler

LANGUAGE = "breton"
MUTATION_HANDLER = CelticMutationHandler(LANGUAGE)

GRAPHEMES = MUTATION_HANDLER.GRAPHEMES

SOFT_TRIGGERS = MUTATION_HANDLER.soft_triggers
HARD_TRIGGERS = MUTATION_HANDLER.hard_triggers
SPIRANT_TRIGGERS = MUTATION_HANDLER.spirant_triggers
MIXED_TRIGGERS = MUTATION_HANDLER.mixed_triggers
NASAL_TRIGGERS = MUTATION_HANDLER.nasal_triggers
LENITION_TRIGGERS = MUTATION_HANDLER.lenition_triggers
ECLIPSIS_TRIGGERS = MUTATION_HANDLER.eclipsis_triggers

SOFT_MUTATION = MUTATION_HANDLER.soft_map
HARD_MUTATION = MUTATION_HANDLER.hard_map
SPIRANT_MUTATION = MUTATION_HANDLER.spirant_map
MIXED_MUTATION = MUTATION_HANDLER.mixed_map
NASAL_MUTATION = MUTATION_HANDLER.nasal_map
LENITION_MUTATION = MUTATION_HANDLER.lenition_map
ECLIPSIS_MUTATION = MUTATION_HANDLER.eclipsis_map

SPACE = " "
SIGMA_STAR = MUTATION_HANDLER.sigma_star

PREPROCESS = MUTATION_HANDLER.preprocessing
POSTPROCESS = MUTATION_HANDLER.postprocessing

DO_SOFT_MUTATION = cdrewrite(
    SOFT_MUTATION,
    union(SPACE, "[BOS]") + SOFT_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    SIGMA_STAR)
DO_HARD_MUTATION = cdrewrite(
    HARD_MUTATION,
    union(SPACE, "[BOS]") + HARD_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    SIGMA_STAR)
DO_SPIRANT_MUTATION = cdrewrite(
    SPIRANT_MUTATION,
    union(SPACE, "[BOS]") + SPIRANT_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    SIGMA_STAR)
DO_MIXED_MUTATION = cdrewrite(
    MIXED_MUTATION,
    union(SPACE, "[BOS]") + MIXED_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    SIGMA_STAR)
DO_NASAL_MUTATION = cdrewrite(
    NASAL_MUTATION,
    union(SPACE, "[BOS]") + NASAL_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    SIGMA_STAR)
DO_LENITION = cdrewrite(
    LENITION_MUTATION,
    union(SPACE, "[BOS]") + LENITION_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    SIGMA_STAR)
DO_ECLIPSIS = cdrewrite(
    ECLIPSIS_MUTATION,
    union(SPACE, "[BOS]") + ECLIPSIS_TRIGGERS + acceptor(SPACE),
    GRAPHEMES,
    SIGMA_STAR)

MUTATION_DICT = {
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
    SIGMA_STAR)

DO_POSTPROCESSING = cdrewrite(
    POSTPROCESS,
    union(SPACE, "[BOS]"),
    union(GRAPHEMES, SPACE),
    SIGMA_STAR)


def preprocess(string: str) -> str:
    """Preprocess the string before normalization."""
    return compose(string.strip().lower(), DO_PREPROCESSING).string()


def postprocess(string: str) -> str:
    """Postprocess the string after normalization."""
    return compose(string, DO_POSTPROCESSING).string()


def apply_mutation(string: str, mutation: str) -> str:
    """Applies a single mutation to a string."""
    applied_mutation = compose(string, MUTATION_DICT.get(mutation)).string()
    return applied_mutation


def normalize_breton(breton_string: str) -> str:
    """Applies Breton mutations."""
    preprocessed_string = preprocess(breton_string)
    apply_soft_mutation = apply_mutation(preprocessed_string, "soft")
    apply_hard_mutation = apply_mutation(apply_soft_mutation, "hard")
    apply_spirant_mutation = apply_mutation(apply_hard_mutation, "spirant")
    postprocessed_string = postprocess(apply_spirant_mutation)
    return postprocessed_string


def normalize_welsh(welsh_string: str) -> str:
    """Applies Welsh mutations."""
    preprocessed_string = preprocess(welsh_string)
    apply_soft_mutation = apply_mutation(preprocessed_string, "soft")
    apply_nasal_mutation = apply_mutation(apply_soft_mutation, "nasal")
    apply_spirant_mutation = apply_mutation(apply_nasal_mutation, "spirant")
    postprocessed_string = postprocess(apply_spirant_mutation)
    return postprocessed_string
