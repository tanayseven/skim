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

from typing import Iterator, NewType, Tuple, Dict, Union, Optional

from skim.types import WordAsInt

Token = NewType("Token", str)


class WordToNumberMap:
    def __init__(self):
        self._count = WordAsInt(0)
        self._number_to_word_map: Dict[WordAsInt, Token] = {}
        self._word_to_number_map: Dict[Token, WordAsInt] = {}

    def add_word(self, word: Token) -> WordAsInt:
        if word not in self._word_to_number_map.keys():
            self._word_to_number_map[word] = self._count
            self._number_to_word_map[self._count] = word
            self._count += 1
        return self._word_to_number_map[word]

    def number_for_word(self, word: Token) -> Optional[WordAsInt]:
        return (
            self._word_to_number_map[word]
            if word in self._word_to_number_map.keys()
            else None
        )

    def word_for_number(self, number: WordAsInt) -> Optional[Token]:
        return (
            self._number_to_word_map[number]
            if number in self._number_to_word_map.keys()
            else None
        )

    def delete_word(self, key: Union[Token, WordAsInt]) -> None:
        if isinstance(key, str):
            number = self._word_to_number_map[Token(key)]
            del self._word_to_number_map[Token(key)]
            del self._number_to_word_map[WordAsInt(number)]
        if isinstance(key, int):
            word = self._number_to_word_map[WordAsInt(key)]
            del self._number_to_word_map[WordAsInt(key)]
            del self._word_to_number_map[word]

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
