#!/usr/bin/env python
"""Library of FST rewrite rules to handle Celtic initial consonant mutations."""

from pynini import *
import mutation_handler

LANGUAGE = "breton"
MUTATION_HANDLER = mutation_handler.CelticMutationHandler(LANGUAGE)

GRAPHEMES = MUTATION_HANDLER.graphemes

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


def normalize_breton(breton_string: str) -> str:
    """Applies Breton mutations."""
    return (breton_string.strip().lower() @
            DO_PREPROCESSING @
            DO_SOFT_MUTATION @
            DO_HARD_MUTATION @
            DO_SPIRANT_MUTATION @
            DO_POSTPROCESSING).string()

def normalize_welsh(welsh_string: str) -> str:
    """Applies Welsh mutations."""
    return (welsh_string.strip().lower() @
            DO_PREPROCESSING @
            DO_SOFT_MUTATION @
            DO_NASAL_MUTATION @
            DO_SPIRANT_MUTATION).string()
