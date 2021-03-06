# Lint as: python3
"""
A class for Celtic initial consonant mutations.
"""

from dataclasses import dataclass
from absl import app
from absl import flags
from pynini import *

FLAGS = flags.FLAGS

@dataclass
class CelticMutationHandler:
    """A class containing language-specific info for Celtic consonant mutation.

    Attributes:
        graphemes: A union of strings of the graphemes of the language.
        soft_triggers: A union of strings of soft mutation triggers.
        soft_map: A string_map or union of transducers for the soft mutation.
        hard_triggers: A union of strings of hard mutation triggers.
        hard_map: A string_map or union of transducers for the hard mutation.
        spirant_triggers: A union of strings of spirant mutation triggers.
        spirant_map: A string_map or union of transducers for the spirant mutation.
        mixed_triggers: A union of strings of mixed mutation triggers.
        mixed_map: A string_map or union of transducers for the mixed mutation.
        lenition_triggers: A union of strings of lenition triggers.
        lenition_map: A string_map or union of transducers for lenition.
        eclipsis_triggers: A union of strings of eclipsis triggers.
        eclipsis_map: A string_map or union of transducers for eclipsis.
        preprocessing: A union of language-specific transducers
            for preprocessing a string.
        postprocessing: A union of language-specific transducers
            for postprocessing a string.
        sigma_star: A cyclic, unweighted acceptor representing
            the closure over the alphabet.
    """

    def __init__(self: str) -> None:
        """Initialize attributes to none, other methods will set as needed."""
        self.graphemes = "None"
        self.soft_triggers = "None"
        self.soft_map = "None"
        self.hard_triggers = "None"
        self.hard_map = "None"
        self.spirant_triggers = "None"
        self.spirant_map = "None"
        self.mixed_triggers = "None"
        self.mixed_map = "None"
        self.nasal_triggers = "None"
        self.nasal_map = "None"
        self.lenition_triggers = "None"
        self.lenition_map = "None"
        self.eclipsis_triggers = "None"
        self.eclipsis_map = "None"
        self.preprocessing = "None"
        self.postprocessing = "None"
        self.sigma_star = union(*("[{}]".format(i) for i in range(1, 256))
                                ).optimize().closure()


    def breton_handler(self):
        """Handler for Breton-specific information."""

        self.graphemes = union("a", "b", "ch", "c'h", "d", "e", "f", "g",
                               "h", "i", "j", "k", "l", "m", "n", "o", "p",
                               "r", "s", "t", "u", "v", "w", "y", "z",
                               "â", "ê", "î", "ô", "û", "ù", "ü", "ñ")

        self.soft_triggers = union("da", "dre", "a", "war", "dindan",
                                   "eme", "en ur", "ne", "na", "ra",
                                   "en em", "daou", "div", "pa",
                                   "pe", "an holl", "re",
                                   #"e", "tra", "ez",
                                  )
        self.hard_triggers = union("ho", "az", "da'z",
                                   #"ez",
                                  )
        self.spirant_triggers = union("he", "va", "tri", "teir", "pevar",
                                      "peder", "nav", "hon",
                                      #"ma", "o"
                                     )
        self.mixed_triggers = union("o", "e", "ma")

        self.soft_map = string_map((
            ("p", "b"),
            ("t", "d"),
            ("k", "g"),
            ("gw", "w"),
            ("m", "v"),
            ))
        self.hard_map = string_map((
            ("b", "p"),
            ("d", "t"),
            ("g", "k"),
            ("m", "v"),
            ))
        self.spirant_map = string_map((
            ("p", "f"),
            ("t", "z"),
            ("k", "c'h"),
            ))
        self.mixed_map = string_map((
            ("b", "v"),
            ("d", "t"),
            ("gw", "w"),
            ("g", "c'h"),
            ("m", "v"),
            ))

        self.preprocessing = union(
            transducer("a ra", "aaaaara"))
        self.postprocessing = union(
            transducer("aaaaara", "a ra"),
            transducer("dre va", "dre ma"),
            )

    # Welsh is an incomplete placeholder to demonstrate how we can use this
    # class for implementing initial consonant mutations for the other
    # Celtic languages.
    def welsh_handler(self):
        """Handler for Welsh-specific information."""

        self.graphemes = union("a", "b", "ch", "d", "e", "f", "g", "h", "i",
                               "j", "k", "l", "m", "n", "o", "p", "r", "s",
                               "t", "u", "w", "y",
                               "â", "ê", "î", "ô", "û", "ŵ", "ŷ", )

        self.soft_triggers = union("dau", "dwy")
        self.nasal_triggers = union("fy")
        self.spirant_triggers = union("gyda", "chwe")

        self.soft_map = string_map((
            ("p", "b"),
            ("ts", "j"),
            ("t", "d"),
            ("c", "g"),
            ("m", "f"),
            ("ll", "l"),
            ("rh", "r"),
            ))
        self.nasal_map = string_map((
            ("p", "mh"),
            ("t", "nh"),
            ("c", "ngh"),
            ("b", "m"),
            ("d", "n"),
            ("g", "ng"),
            ))
        self.spirant_map = string_map((
            ("p", "ph"),
            ("t", "th"),
            ("c", "ch"),
            ))

        self.preprocessing = union(
            transducer("cath", "cath"))
        self.postprocessing = union(
            transducer("heddiw", "heddiw"),
            transducer("cwmwl", "cwmwl"),
            )


def main(argv):
    if len(argv) > 1:
        raise app.UsageError('Too many command-line arguments.')

if __name__ == '__main__':
    app.run(main)
