import unicodedata
from typing import List

SPACE_CATEGORY = unicodedata.category(" ")


def tokenize(input_string: str) -> List[str]:
    normalized_input_string = unicodedata.normalize("NFD", input_string)
    all_space_chars = (
        "".join(
            char
            for char in normalized_input_string
            if unicodedata.category(char) == SPACE_CATEGORY
        )
        or None
    )
    return normalized_input_string.split(all_space_chars)
