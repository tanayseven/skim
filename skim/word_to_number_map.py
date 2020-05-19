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
from typing import Iterator, NewType, Tuple, Dict

from skim.exceptions import WordNotFoundError
from skim.types import PossiblePrediction

WordType = NewType("WordType", str)


class WordToNumberMap(MutableMapping):
    def __setitem__(self, key: None, value: None) -> None:
        raise NotImplementedError("Cannot set your own number to a word")

    def __delitem__(self, key: WordType) -> None:
        if key not in self._word_map.keys():
            raise WordNotFoundError
        del self._word_map[key]

    def __init__(self):
        self._count = PossiblePrediction(0)
        self._word_map: Dict[WordType, PossiblePrediction] = {}

    def __getitem__(self, key: WordType) -> PossiblePrediction:
        if key not in self._word_map.keys():
            self._word_map[key] = self._count
            self._count += 1
        return self._word_map[key]

    def __len__(self) -> int:
        return len(self._word_map.keys())

    def __iter__(self) -> Iterator[Tuple[WordType, PossiblePrediction]]:
        return iter(
            (word_type, possible_prediction)
            for word_type, possible_prediction in self._word_map.items()
        )
