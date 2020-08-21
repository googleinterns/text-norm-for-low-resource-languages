"Amharic config with language-specific information."

from pynini import *
from pynini.lib import byte
from config import utils

GRAPHEMES = union("'", "-",
                  "ሀ", "ሁ", "ሂ", "ሃ", "ሄ", "ህ", "ሆ",
                  "ለ", "ሉ", "ሊ", "ላ", "ሌ", "ል", "ሎ", "ሏ",
                  "ሐ", "ሑ", "ሒ", "ሓ", "ሔ", "ሕ", "ሖ", "ሗ",
                  "መ", "ሙ", "ሚ", "ማ", "ሜ", "ም", "ሞ", "ሟ",
                  "ሠ", "ሡ", "ሢ", "ሣ", "ሤ", "ሥ", "ሦ", "ሧ",
                  "ረ", "ሩ", "ሪ", "ራ", "ሬ", "ር", "ሮ", "ሯ",
                  "ሰ", "ሱ", "ሲ", "ሳ", "ሴ", "ስ", "ሶ", "ሷ",
                  "ሸ", "ሹ", "ሺ", "ሻ", "ሼ", "ሽ", "ሾ", "ሿ",
                  "ቀ", "ቁ", "ቂ", "ቃ", "ቄ", "ቅ",
                  "ቆ", "ቈ", "ቊ", "ቋ", "ቌ", "ቍ",
                  "በ", "ቡ", "ቢ", "ባ", "ቤ", "ብ", "ቦ", "ቧ",
                  "ቨ", "ቩ", "ቪ", "ቫ", "ቬ", "ቭ", "ቮ", "ቯ",
                  "ተ", "ቱ", "ቲ", "ታ", "ቴ", "ት", "ቶ", "ቷ",
                  "ቸ", "ቹ", "ቺ", "ቻ", "ቼ", "ች", "ቾ", "ቿ",
                  "ኀ", "ኁ", "ኂ", "ኃ", "ኄ", "ኅ",
                  "ኆ", "ኈ", "ኊ", "ኋ", "ኌ", "ኍ",
                  "ነ", "ኑ", "ኒ", "ና", "ኔ", "ን", "ኖ", "ኗ",
                  "ኘ", "ኙ", "ኚ", "ኛ", "ኜ", "ኝ", "ኞ", "ኟ",
                  "አ", "ኡ", "ኢ", "ኣ", "ኤ", "እ", "ኦ", "ኧ",
                  "ከ", "ኩ", "ኪ", "ካ", "ኬ", "ክ",
                  "ኮ", "ኰ", "ኲ", "ኳ", "ኴ", "ኵ",
                  "ኸ", "ኹ", "ኺ", "ኻ", "ኼ", "ኽ",
                  "ኾ", "ዀ", "ዂ", "ዃ", "ዄ", "ዅ",
                  "ወ", "ዉ", "ዊ", "ዋ", "ዌ", "ው", "ዎ",
                  "ዐ", "ዑ", "ዒ", "ዓ", "ዔ", "ዕ", "ዖ",
                  "ዘ", "ዙ", "ዚ", "ዛ", "ዜ", "ዝ", "ዞ", "ዟ",
                  "ዠ", "ዡ", "ዢ", "ዣ", "ዤ", "ዥ", "ዦ", "ዧ",
                  "የ", "ዩ", "ዪ", "ያ", "ዬ", "ይ", "ዮ",
                  "ደ", "ዱ", "ዲ", "ዳ", "ዴ", "ድ", "ዶ", "ዷ",
                  "ጀ", "ጁ", "ጂ", "ጃ", "ጄ", "ጅ", "ጆ", "ጇ",
                  "ገ", "ጉ", "ጊ", "ጋ", "ጌ", "ግ",
                  "ጎ", "ጐ", "ጒ", "ጓ", "ጔ", "ጕ",
                  "ጠ", "ጡ", "ጢ", "ጣ", "ጤ", "ጥ", "ጦ", "ጧ",
                  "ጨ", "ጩ", "ጪ", "ጫ", "ጬ", "ጭ", "ጮ", "ጯ",
                  "ጰ", "ጱ", "ጲ", "ጳ", "ጴ", "ጵ", "ጶ", "ጷ",
                  "ጸ", "ጹ", "ጺ", "ጻ", "ጼ", "ጽ", "ጾ", "ጿ",
                  "ፀ", "ፁ", "ፂ", "ፃ", "ፄ", "ፅ", "ፆ",
                  "ፈ", "ፉ", "ፊ", "ፋ", "ፌ", "ፍ", "ፎ", "ፏ",
                  "ፐ", "ፑ", "ፒ", "ፓ", "ፔ", "ፕ", "ፖ", "ፗ")

INITIAL_PUNCTUATION = utils.DEFAULT_INITIAL_PUNCTUATION

FINAL_PUNCTUATION = union(utils.DEFAULT_FINAL_PUNCTUATION,
                          utils.GEEZ_FINAL_PUNCTUATION)

NUMERALS = union(byte.DIGIT,
                 utils.GEEZ_NUMERALS)

# Amharic "over-differentiates" H graphemes, emphatic S graphemes, and glottal
# stop graphemes, which were all inherited from Ge'ez. Surveys suggest that
# Amharic speakers prefer one form over the others. These rules convert the
# dispreferred series graphemes to the one preferred series, when available.
# The surveys about grapheme preference come from the paper here:
# https://www.researchgate.net/profile/Fekede_Menuta/publication/312093656_OVER-DIFFERENTIATION_3_Over-differentiation_in_Amharic_Orthography_and_Attitude_towards_Reform/links/586f5d8408ae329d6215fb85/OVER-DIFFERENTIATION-3-Over-differentiation-in-Amharic-Orthography-and-Attitude-towards-Reform.pdf
REDUCE_H = string_map((("ሐ", "ሀ"),
                       ("ሑ", "ሁ"),
                       ("ሒ", "ሂ"),
                       ("ሓ", "ሂ"),
                       ("ሔ", "ሄ"),
                       ("ሕ", "ህ"),
                       ("ሖ", "ሆ"),
                       #("ሗ", "")

                       ("ኀ", "ሀ"),
                       ("ኁ", "ሁ"),
                       ("ኂ", "ሂ"),
                       ("ኃ", "ሂ"),
                       ("ኄ", "ሄ"),
                       ("ኅ", "ህ"),
                       ("ኆ", "ሆ"),
                       #("ኈ", ""),
                       #("ኊ", ""),
                       #("ኋ", ""),
                       #("ኌ", ""),
                       #("ኍ", ""),

                       ("ኸ", "ሀ"),
                       ("ኹ", "ሁ"),
                       ("ኺ", "ሂ"),
                       ("ኻ", "ሂ"),
                       ("ኼ", "ሄ"),
                       ("ኽ", "ህ"),
                       ("ኾ", "ሆ")
                       #("ዀ", ""),
                       #("ዂ", ""),
                       #("ዃ", ""),
                       #("ዄ", ""),
                       #("ዅ", "")
                       ))

REDUCE_S = string_map((("ጸ", "ፀ"),
                       ("ጹ", "ፁ"),
                       ("ጺ", "ፂ"),
                       ("ጻ", "ፃ"),
                       ("ጼ", "ፄ"),
                       ("ጽ", "ፅ"),
                       ("ጾ", "ፆ")
                       #("ጿ", "")
                       ))

REDUCE_A = string_map((("ዐ", "አ"),
                       ("ዑ", "አ"),
                       ("ዒ", "ኢ"),
                       ("ዓ", "ኣ"),
                       ("ዔ", "ኤ"),
                       ("ዕ", "እ"),
                       ("ዖ", "ኦ")
                       ))

REDUCE_OVERDIFFERENTIATION = cdrewrite(
    union(REDUCE_H, REDUCE_S, REDUCE_A),
    "",
    "",
    byte.BYTES.closure())

LANGUAGE_SPECIFIC_PREPROCESSING = REDUCE_OVERDIFFERENTIATION

UD = "language_data/am/UD_Amharic-ATT/am_att-ud-test.conllu"
UM = ""
AC = "language_data/am/ac/am-wordbigrams.txt"
OSCAR = "language_data/am/oscar/am.txt"
OSCAR_DEDUP = "language_data/am/oscar/am_dedup.txt"
LCC = "language_data/am/lcc/amh_wikipedia_2016_30K/amh_wikipedia_2016_30K-sentences.txt"
