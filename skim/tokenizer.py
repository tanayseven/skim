import unicodedata
from typing import List

SPACE_CATEGORY = unicodedata.category(" ")
PUNCTUATION_CATEGORY = unicodedata.category(".")


def tokenize(input_string: str) -> List[str]:
    normalized_input_string = unicodedata.normalize("NFD", input_string)
    normalized_and_separated_punctuations = "".join(
        f" {char}" if unicodedata.category(char) == PUNCTUATION_CATEGORY else f"{char}"
        for char in normalized_input_string
    )
    all_space_chars = (
        "".join(
            char
            for char in normalized_input_string
            if unicodedata.category(char) == SPACE_CATEGORY
        )
        or ""
    )
    unique_all_space_chars = "".join(set(all_space_chars))
    return normalized_and_separated_punctuations.split(unique_all_space_chars or None)
