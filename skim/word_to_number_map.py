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

from collections.abc import MutableMapping
from typing import Iterator, NewType, Tuple, Dict, Union

from skim.exceptions import WordNotFoundError
from skim.types import WordAsInt

Token = NewType("Token", str)


class WordToNumberMap(MutableMapping):
    def __setitem__(self, key: None, value: None) -> None:
        raise NotImplementedError("Cannot set your own number to a word")

    def __delitem__(self, key: Token) -> None:
        if key not in self._number_to_word_map.keys():
            raise WordNotFoundError
        del self._number_to_word_map[key]

    def __init__(self):
        self._count = WordAsInt(0)
        self._number_to_word_map: Dict[
            Union[Token, WordAsInt], Union[Token, WordAsInt]
        ] = {}

    def __getitem__(self, key: Union[Token, WordAsInt]) -> Union[Token, WordAsInt]:
        if type(key) == WordAsInt and key not in self._number_to_word_map.keys():
            raise KeyError(f"Could not find the token for the WordAsInt({key})")
        if key not in self._number_to_word_map.keys():
            self._number_to_word_map[key] = self._count
            self._number_to_word_map[self._count] = key
            self._count += 1
        return self._number_to_word_map[key]

    def __len__(self) -> int:
        return len(self._number_to_word_map.keys())

    def __iter__(
        self,
    ) -> Iterator[Tuple[Union[Token, WordAsInt], Union[Token, WordAsInt]]]:
        return iter(
            (word_type, possible_prediction)
            for word_type, possible_prediction in self._number_to_word_map.items()
            if type(word_type) == Token and type(possible_prediction) == WordAsInt
        )
