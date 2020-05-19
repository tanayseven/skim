# SKIM | Smarter Keyboard Input Method | A simple and smart sentence prediction
# Copyright (C) 2020 Tanay PrabhuDesai

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
